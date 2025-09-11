"""FastAPI application for the Legendary AI Training System."""

import asyncio
from contextlib import asynccontextmanager
from typing import Dict, List, Optional

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import StreamingResponse
    from pydantic import BaseModel
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False

from ..training import (
    TrainingProfile,
    create_legendary_agent,
    get_training_profile,
)
from ..run import Runner


if FASTAPI_AVAILABLE:
    
    # Pydantic models for API
    class ChatRequest(BaseModel):
        message: str
        profile: str = "balanced_expert"
        stream: bool = False
        
    
    class ChatResponse(BaseModel):
        response: str
        profile_name: str
        agent_name: str
        
    
    class ProfileInfo(BaseModel):
        name: str
        description: str
        intensity: str
        focus: str
        skill_domains: List[str]
        
    
    class ProfilesResponse(BaseModel):
        profiles: List[ProfileInfo]
        
    
    class ErrorResponse(BaseModel):
        error: str
        detail: str
        

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """Application lifespan manager."""
        # Startup
        print("🚀 Legendary AI Training API starting up...")
        yield
        # Shutdown
        print("👋 Legendary AI Training API shutting down...")


    def create_app() -> FastAPI:
        """Create and configure the FastAPI application."""
        
        app = FastAPI(
            title="Legendary AI Training System API",
            description="REST API for the OpenAI Agents SDK with Legendary Training capabilities",
            version="1.0.0",
            lifespan=lifespan
        )
        
        # Add CORS middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Configure appropriately for production
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        
        @app.get("/", summary="API Information")
        async def root():
            """Get API information."""
            return {
                "name": "Legendary AI Training System API",
                "version": "1.0.0",
                "description": "REST API for creating and interacting with legendary AI agents",
                "endpoints": {
                    "/profiles": "List all available training profiles",
                    "/profiles/{profile_name}": "Get specific profile information",
                    "/chat": "Chat with a legendary AI agent",
                    "/chat/stream": "Stream chat with a legendary AI agent",
                    "/health": "API health check"
                }
            }
        
        
        @app.get("/health", summary="Health Check")
        async def health_check():
            """Health check endpoint."""
            return {
                "status": "healthy",
                "service": "legendary-training-api",
                "version": "1.0.0"
            }
        
        
        @app.get("/profiles", response_model=ProfilesResponse, summary="List Training Profiles")
        async def list_profiles():
            """List all available legendary training profiles."""
            
            profile_names = [
                "legendary_sage",
                "analytical_master", 
                "communication_expert",
                "innovation_genius",
                "ethical_leader",
                "balanced_expert"
            ]
            
            profiles = []
            for profile_name in profile_names:
                try:
                    profile = get_training_profile(profile_name)
                    profiles.append(ProfileInfo(
                        name=profile.name,
                        description=profile.description,
                        intensity=profile.intensity.value,
                        focus=profile.focus.value,
                        skill_domains=list(profile.skill_domains)
                    ))
                except Exception as e:
                    # Skip invalid profiles
                    continue
            
            return ProfilesResponse(profiles=profiles)
        
        
        @app.get("/profiles/{profile_name}", response_model=ProfileInfo, summary="Get Profile Info")
        async def get_profile_info(profile_name: str):
            """Get information about a specific training profile."""
            
            try:
                profile = get_training_profile(profile_name)
                return ProfileInfo(
                    name=profile.name,
                    description=profile.description,
                    intensity=profile.intensity.value,
                    focus=profile.focus.value,
                    skill_domains=list(profile.skill_domains)
                )
            except ValueError:
                raise HTTPException(
                    status_code=404,
                    detail=f"Training profile '{profile_name}' not found"
                )
        
        
        @app.post("/chat", response_model=ChatResponse, summary="Chat with Legendary Agent")
        async def chat(request: ChatRequest):
            """Chat with a legendary AI agent."""
            
            try:
                # Get the training profile
                profile = get_training_profile(request.profile)
                
                # Create the legendary agent
                agent = create_legendary_agent(
                    name=f"Legendary {profile.name}",
                    profile=profile
                )
                
                # Run the agent
                result = await Runner.run(agent, request.message)
                
                return ChatResponse(
                    response=result.final_output,
                    profile_name=profile.name,
                    agent_name=agent.name
                )
                
            except ValueError as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid training profile: {str(e)}"
                )
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error processing request: {str(e)}"
                )
        
        
        @app.post("/chat/stream", summary="Stream Chat with Legendary Agent")
        async def chat_stream(request: ChatRequest):
            """Stream chat responses from a legendary AI agent."""
            
            try:
                # Get the training profile
                profile = get_training_profile(request.profile)
                
                # Create the legendary agent
                agent = create_legendary_agent(
                    name=f"Legendary {profile.name}",
                    profile=profile
                )
                
                async def generate_stream():
                    """Generate streaming response."""
                    try:
                        result_stream = Runner.run_streamed(agent, request.message)
                        
                        async for event in result_stream.stream_events():
                            if hasattr(event, 'type') and hasattr(event, 'data'):
                                yield f"data: {event.data}\n\n"
                            else:
                                # Fallback for different event types
                                yield f"data: {str(event)}\n\n"
                                
                    except Exception as e:
                        yield f"data: {{\"error\": \"{str(e)}\"}}\n\n"
                    
                    yield "data: [DONE]\n\n"
                
                return StreamingResponse(
                    generate_stream(),
                    media_type="text/plain",
                    headers={
                        "Cache-Control": "no-cache",
                        "Connection": "keep-alive",
                    }
                )
                
            except ValueError as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid training profile: {str(e)}"
                )
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error processing request: {str(e)}"
                )
        
        
        return app

else:
    # FastAPI not available
    def create_app():
        """Create app when FastAPI is not available."""
        raise ImportError(
            "FastAPI is not installed. Install it with: pip install 'agents[api]'"
        )