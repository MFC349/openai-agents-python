import asyncio
import base64
import json
import logging
import struct
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from typing_extensions import assert_never

from agents.realtime import RealtimeRunner, RealtimeSession, RealtimeSessionEvent

# Import TwilioHandler class - handle both module and package use cases
if TYPE_CHECKING:
    # For type checking, use the relative import
    from .agent import get_starting_agent
else:
    # At runtime, try both import styles
    try:
        # Try relative import first (when used as a package)
        from .agent import get_starting_agent
    except ImportError:
        # Fall back to direct import (when run as a script)
        from agent import get_starting_agent


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RealtimeWebSocketManager:
    def __init__(self):
        self.active_sessions: dict[str, RealtimeSession] = {}
        self.session_contexts: dict[str, Any] = {}
        self.websockets: dict[str, WebSocket] = {}
        self._pending_audio: dict[str, bytearray] = {}
        self._audio_flush_tasks: dict[str, asyncio.Task[Any]] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.websockets[session_id] = websocket

        agent = get_starting_agent()
        runner = RealtimeRunner(agent)
        # Disable server-side interrupt_response to avoid truncating assistant audio
        session_context = await runner.run(
            model_config={
                "initial_model_settings": {
                    "turn_detection": {"type": "semantic_vad", "interrupt_response": False}
                }
            }
        )
        session = await session_context.__aenter__()
        self.active_sessions[session_id] = session
        self.session_contexts[session_id] = session_context

        # Start event processing task
        asyncio.create_task(self._process_events(session_id))
        # Init audio buffer + steady flush task (~40ms)
        self._pending_audio[session_id] = bytearray()
        self._audio_flush_tasks[session_id] = asyncio.create_task(self._flush_audio_loop(session_id))

    async def disconnect(self, session_id: str):
        if session_id in self.session_contexts:
            await self.session_contexts[session_id].__aexit__(None, None, None)
            del self.session_contexts[session_id]
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
        if session_id in self.websockets:
            del self.websockets[session_id]
        if session_id in self._pending_audio:
            del self._pending_audio[session_id]
        if session_id in self._audio_flush_tasks:
            self._audio_flush_tasks[session_id].cancel()
            del self._audio_flush_tasks[session_id]

    async def send_audio(self, session_id: str, audio_bytes: bytes):
        if session_id in self.active_sessions:
            await self.active_sessions[session_id].send_audio(audio_bytes)

    async def _process_events(self, session_id: str):
        try:
            session = self.active_sessions[session_id]
            websocket = self.websockets[session_id]

            async for event in session:
                event_data = await self._serialize_event(session_id, event)
                if event_data is not None:
                    await websocket.send_text(json.dumps(event_data))
        except Exception as e:
            logger.error(f"Error processing events for session {session_id}: {e}")

    async def _serialize_event(self, session_id: str, event: RealtimeSessionEvent) -> dict[str, Any] | None:
        base_event: dict[str, Any] = {
            "type": event.type,
        }

        if event.type == "agent_start":
            base_event["agent"] = event.agent.name
        elif event.type == "agent_end":
            base_event["agent"] = event.agent.name
        elif event.type == "handoff":
            base_event["from"] = event.from_agent.name
            base_event["to"] = event.to_agent.name
        elif event.type == "tool_start":
            base_event["tool"] = event.tool.name
        elif event.type == "tool_end":
            base_event["tool"] = event.tool.name
            base_event["output"] = str(event.output)
        elif event.type == "audio":
            # Coalesce raw PCM and flush on a steady timer for smoother playback.
            self._pending_audio[session_id].extend(event.audio.data)
            return None
        elif event.type == "audio_interrupted":
            pass
        elif event.type == "audio_end":
            pass
        elif event.type == "history_updated":
            base_event["history"] = [item.model_dump(mode="json") for item in event.history]
        elif event.type == "history_added":
            pass
        elif event.type == "guardrail_tripped":
            base_event["guardrail_results"] = [
                {"name": result.guardrail.name} for result in event.guardrail_results
            ]
        elif event.type == "raw_model_event":
            # Surface useful raw events to the UI with details.
            if getattr(event.data, "type", None) == "transcript_delta":
                # Stream assistant transcript deltas to the UI.
                base_event = {
                    "type": "transcript_delta",
                    "item_id": getattr(event.data, "item_id", ""),
                    "response_id": getattr(event.data, "response_id", ""),
                    "delta": getattr(event.data, "delta", ""),
                }
            else:
                # Fallback to a minimal raw event descriptor.
                base_event["raw_model_event"] = {
                    "type": getattr(event.data, "type", "other"),
                }
        elif event.type == "error":
            base_event["error"] = str(event.error) if hasattr(event, "error") else "Unknown error"
        elif event.type == "input_audio_timeout_triggered":
            pass
        else:
            assert_never(event)

        return base_event

    async def _flush_audio_loop(self, session_id: str) -> None:
        try:
            while session_id in self.websockets:
                await asyncio.sleep(0.04)  # ~40ms cadence
                buf = self._pending_audio.get(session_id)
                ws = self.websockets.get(session_id)
                if not buf or ws is None:
                    continue
                if not buf:
                    continue
                b = bytes(buf)
                self._pending_audio[session_id] = bytearray()
                try:
                    await ws.send_text(
                        json.dumps({"type": "audio", "audio": base64.b64encode(b).decode("utf-8")})
                    )
                except Exception:
                    logger.error("Failed sending coalesced audio", exc_info=True)
                    break
        except asyncio.CancelledError:
            pass


manager = RealtimeWebSocketManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await manager.connect(websocket, session_id)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            if message["type"] == "audio":
                # Convert int16 array to bytes
                int16_data = message["data"]
                # Send little-endian PCM16 to the model.
                audio_bytes = struct.pack("<" + f"{len(int16_data)}h", *int16_data)
                await manager.send_audio(session_id, audio_bytes)

    except WebSocketDisconnect:
        await manager.disconnect(session_id)


app.mount("/", StaticFiles(directory="static", html=True), name="static")


@app.get("/")
async def read_index():
    return FileResponse("static/index.html")


if __name__ == "__main__":
    import uvicorn

    log_level = "info"
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level=log_level)
