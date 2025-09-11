"""Main CLI application for OpenAI Agents SDK with Legendary Training System."""

import asyncio
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ..training import (
    TrainingIntensity,
    TrainingProfile,
    create_legendary_agent,
    get_training_profile,
)
from ..run import Runner

app = typer.Typer(help="OpenAI Agents SDK with Legendary Training System")
console = Console()


@app.command("list-profiles")
def list_training_profiles():
    """List all available legendary training profiles."""
    profiles = {
        "legendary_sage": "Master-level capabilities across all domains",
        "analytical_master": "Exceptional analytical and problem-solving abilities", 
        "communication_expert": "Master communicator and interpersonal specialist",
        "innovation_genius": "Creative problem-solver and innovation catalyst",
        "ethical_leader": "Principled leader with strong moral reasoning",
        "balanced_expert": "Well-rounded expert with advanced capabilities"
    }
    
    table = Table(title="🎯 Available Legendary Training Profiles")
    table.add_column("Profile", style="cyan", no_wrap=True)
    table.add_column("Description", style="magenta")
    table.add_column("Intensity", style="green")
    
    for profile_name, description in profiles.items():
        try:
            profile = get_training_profile(profile_name)
            intensity = profile.intensity.value if hasattr(profile.intensity, 'value') else str(profile.intensity)
            table.add_row(profile_name, description, intensity)
        except Exception:
            table.add_row(profile_name, description, "legendary")
    
    console.print(table)
    console.print("\n💡 Use 'agents chat <profile>' to interact with a legendary agent")


@app.command("chat")
def chat_with_agent(
    profile: str = typer.Argument(help="Training profile to use"),
    message: Optional[str] = typer.Option(None, "-m", "--message", help="Initial message to send"),
    no_interactive: bool = typer.Option(False, "--no-interactive", help="Disable interactive mode")
):
    """Chat with a legendary AI agent using the specified training profile."""
    
    try:
        # Get the training profile
        training_profile = get_training_profile(profile)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("\n💡 Use 'agents list-profiles' to see available profiles")
        return
    
    # Create the legendary agent
    agent = create_legendary_agent(
        name=f"Legendary {training_profile.name}",
        profile=training_profile
    )
    
    console.print(Panel(
        f"🚀 [bold cyan]{agent.name}[/bold cyan]\n"
        f"[dim]{training_profile.description}[/dim]\n\n"
        f"Intensity: [green]{training_profile.intensity.value}[/green]\n"
        f"Focus: [yellow]{training_profile.focus.value}[/yellow]\n"
        f"Domains: [blue]{', '.join(training_profile.skill_domains)}[/blue]",
        title="Legendary Agent Ready",
        border_style="green"
    ))
    
    if message:
        # Run single message
        asyncio.run(_run_single_message(agent, message))
    elif not no_interactive:
        # Start interactive session
        asyncio.run(_run_interactive_session(agent))


async def _run_single_message(agent, message: str):
    """Run a single message through the agent."""
    console.print(f"\n[bold]You:[/bold] {message}")
    console.print("\n[bold]Legendary Agent:[/bold]")
    
    try:
        result = await Runner.run(agent, message)
        console.print(Panel(result.final_output, border_style="blue"))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


async def _run_interactive_session(agent):
    """Run an interactive chat session."""
    console.print("\n💬 [dim]Starting interactive session. Type 'quit', 'exit', or press Ctrl+C to end.[/dim]\n")
    
    try:
        while True:
            # Get user input
            user_input = typer.prompt("\nYou")
            
            if user_input.lower() in ['quit', 'exit']:
                console.print("\n👋 [dim]Ending session. Farewell![/dim]")
                break
            
            # Process with agent
            console.print("\n[bold]Legendary Agent:[/bold]")
            try:
                result = await Runner.run(agent, user_input)
                console.print(Panel(result.final_output, border_style="blue"))
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
                
    except KeyboardInterrupt:
        console.print("\n\n👋 [dim]Session interrupted. Farewell![/dim]")


@app.command("demo")
def run_demo(
    profile: Optional[str] = typer.Option(None, "-p", "--profile", help="Specific profile to demo")
):
    """Run the legendary training system demonstration."""
    
    if profile:
        # Demo specific profile
        try:
            training_profile = get_training_profile(profile)
            console.print(f"\n🎯 [bold]Demonstrating {training_profile.name}[/bold]")
            asyncio.run(_demo_profile(training_profile))
        except ValueError as e:
            console.print(f"[red]Error: {e}[/red]")
            return
    else:
        # Run full demo
        console.print(Panel(
            "🚀 [bold]Legendary AI Training System Demonstration[/bold]\n\n"
            "This demo showcases how legendary training transforms AI agents with "
            "master-level capabilities across multiple domains of knowledge and skill.",
            title="Welcome to Legendary Training",
            border_style="green"
        ))
        
        # Import and run the main demo
        try:
            import sys
            import os
            # Add the project root to the path
            project_root = os.path.join(os.path.dirname(__file__), '..', '..', '..')
            sys.path.insert(0, project_root)
            
            from examples.legendary_training.main import main
            asyncio.run(main())
        except ImportError:
            console.print("[yellow]⚠️  Full demo module not available. Running basic demo...[/yellow]")
            asyncio.run(_demo_all_profiles())


async def _demo_profile(profile: TrainingProfile):
    """Demo a specific training profile."""
    
    # Create agent
    agent = create_legendary_agent(f"Demo {profile.name}", profile)
    
    # Sample challenge based on profile focus
    challenges = {
        "legendary_sage": "How would you approach solving climate change while balancing economic growth, social equity, and environmental protection?",
        "analytical_master": "Analyze the potential long-term impacts of artificial intelligence on society, considering technological, economic, and ethical dimensions.",
        "communication_expert": "Explain blockchain technology to three different audiences: a 10-year-old, a business executive, and a technical developer.",
        "innovation_genius": "Design innovative solutions for reducing urban traffic congestion without traditional infrastructure expansion.",
        "ethical_leader": "How should organizations handle AI bias in hiring while maintaining efficiency and legal compliance?",
        "balanced_expert": "What framework would you use to make a complex life decision involving career change, family impact, and financial considerations?"
    }
    
    challenge = challenges.get(
        profile.name.lower().replace(" ", "_").replace("-", "_"),
        "Share your thoughts on how to approach complex, multi-faceted challenges that require wisdom across multiple domains."
    )
    
    console.print(f"\n[bold]Challenge:[/bold] {challenge}")
    console.print(f"\n[bold]{agent.name} Response:[/bold]")
    
    try:
        result = await Runner.run(agent, challenge)
        console.print(Panel(result.final_output, border_style="cyan"))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@app.command("info")
def show_info():
    """Show information about the legendary training system."""
    
    info_text = """
🎯 [bold]Legendary AI Training System[/bold]

The Legendary AI Training System transforms ordinary AI agents into masters with
exceptional capabilities across multiple domains of human knowledge and expertise.

[bold cyan]Key Features:[/bold cyan]
• 🧠 Master-level problem solving and analytical thinking
• 💬 Exceptional communication and interpersonal skills  
• 🎨 Creative innovation and out-of-the-box solutions
• ⚖️  Sophisticated ethical reasoning and moral decision-making
• 👑 Inspirational leadership and mentorship capabilities
• 🔬 Deep expertise across multiple knowledge domains

[bold yellow]Training Intensities:[/bold yellow]
• Basic: Foundational skills and awareness
• Intermediate: Solid capabilities with room to grow
• Advanced: Expert-level performance and insight
• Legendary: Master-level excellence across all dimensions

[bold green]Training Focus Areas:[/bold green]  
• Analytical: Problem-solving, reasoning, analysis
• Interpersonal: Communication, leadership, collaboration
• Creative: Innovation, creative thinking, design
• Ethical: Moral reasoning, ethics, values
• Comprehensive: All domains balanced

[bold magenta]Available Profiles:[/bold magenta]
Use 'agents list-profiles' to see all available legendary training configurations.
"""
    
    console.print(Panel(info_text, title="🚀 Legendary Training System", border_style="blue"))


async def _demo_all_profiles():
    """Demo all training profiles."""
    profiles = ["legendary_sage", "analytical_master", "communication_expert", 
               "innovation_genius", "ethical_leader", "balanced_expert"]
    
    for profile_name in profiles:
        try:
            profile = get_training_profile(profile_name)
            console.print(f"\n{'='*60}")
            console.print(f"🎯 [bold]{profile.name} Demonstration[/bold]")
            console.print(f"{'='*60}")
            await _demo_profile(profile)
        except Exception as e:
            console.print(f"[red]Error demoing {profile_name}: {e}[/red]")


if __name__ == "__main__":
    app()