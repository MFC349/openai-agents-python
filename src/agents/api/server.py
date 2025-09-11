#!/usr/bin/env python3
"""Script to run the Legendary AI Training System API server."""

import os
import sys
from typing import Optional

import typer
from rich.console import Console

try:
    import uvicorn
    UVICORN_AVAILABLE = True
except ImportError:
    UVICORN_AVAILABLE = False

from .main import create_app

console = Console()


def main(
    host: str = typer.Option("0.0.0.0", help="Host to bind the server to"),
    port: int = typer.Option(8000, help="Port to bind the server to"),
    reload: bool = typer.Option(False, help="Enable auto-reload for development"),
    workers: Optional[int] = typer.Option(None, help="Number of worker processes"),
):
    """Run the Legendary AI Training System API server."""
    
    if not UVICORN_AVAILABLE:
        console.print("[red]Error: uvicorn is not installed.[/red]")
        console.print("Install it with: [cyan]pip install 'agents[api]'[/cyan]")
        sys.exit(1)
    
    console.print("[green]🚀 Starting Legendary AI Training System API Server[/green]")
    console.print(f"[dim]Server will be available at: http://{host}:{port}[/dim]")
    console.print(f"[dim]API documentation at: http://{host}:{port}/docs[/dim]\n")
    
    # Check for OpenAI API key
    if not os.environ.get("OPENAI_API_KEY"):
        console.print("[yellow]⚠️  No OPENAI_API_KEY found.[/yellow]")
        console.print("[yellow]   API will use stub responses for demonstration.[/yellow]")
        console.print("[yellow]   Set OPENAI_API_KEY to use real OpenAI models.[/yellow]\n")
    
    try:
        app = create_app()
        
        # Configure uvicorn
        config = {
            "app": app,
            "host": host,
            "port": port,
            "reload": reload,
        }
        
        if workers:
            config["workers"] = workers
        
        uvicorn.run(**config)
        
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 Server stopped by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error running server: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    typer.run(main)