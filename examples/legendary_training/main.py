"""Example usage of the legendary training system.

This example demonstrates how to create and use agents with legendary training
across different scenarios and use cases.
"""

import asyncio

from agents import Agent, Runner
from agents.training import (
    TrainingProfile,
    apply_legendary_training,
    create_legendary_agent,
    get_training_profile,
)


async def demonstrate_legendary_sage():
    """Demonstrate the legendary sage profile - master of all domains."""
    print("=== Legendary Sage Demonstration ===")

    # Create a legendary sage agent
    sage = create_legendary_agent(
        name="The Legendary Sage",
        profile=get_training_profile("legendary_sage")
    )

    # Test complex problem-solving
    result = await Runner.run(
        sage,
        """I'm facing a complex challenge: Our organization needs to transition to sustainable
        practices while maintaining profitability and employee satisfaction. The leadership team
        is divided, some stakeholders are resistant to change, and we have limited time and
        budget. How would you approach this multi-faceted challenge?"""
    )

    print("Sage's Response:")
    print(result.final_output)
    print("\n" + "="*80 + "\n")


async def demonstrate_analytical_master():
    """Demonstrate the analytical master profile."""
    print("=== Analytical Master Demonstration ===")

    # Create an analytical master agent
    analyst = create_legendary_agent(
        name="The Analytical Master",
        profile=get_training_profile("analytical_master")
    )

    # Test analytical reasoning
    result = await Runner.run(
        analyst,
        """Analyze the potential impacts of artificial intelligence on the job market over
        the next 10 years. Consider economic, social, and technological factors. What patterns
        do you see, what assumptions should we question, and what scenarios should we prepare for?"""
    )

    print("Analyst's Response:")
    print(result.final_output)
    print("\n" + "="*80 + "\n")


async def demonstrate_communication_expert():
    """Demonstrate the communication expert profile."""
    print("=== Communication Expert Demonstration ===")

    # Create a communication expert agent
    communicator = create_legendary_agent(
        name="The Communication Expert",
        profile=get_training_profile("communication_expert")
    )

    # Test communication skills
    result = await Runner.run(
        communicator,
        """I need to explain quantum computing to three different audiences:
        1) A 12-year-old curious about science
        2) Business executives evaluating investment opportunities
        3) University computer science students
        How would you adapt the explanation for each audience?"""
    )

    print("Communicator's Response:")
    print(result.final_output)
    print("\n" + "="*80 + "\n")


async def demonstrate_innovation_genius():
    """Demonstrate the innovation genius profile."""
    print("=== Innovation Genius Demonstration ===")

    # Create an innovation genius agent
    innovator = create_legendary_agent(
        name="The Innovation Genius",
        profile=get_training_profile("innovation_genius")
    )

    # Test creative problem-solving
    result = await Runner.run(
        innovator,
        """We need creative solutions for reducing food waste in urban areas. The challenge
        is that food waste happens at multiple points: production, distribution, retail, and
        consumption. How might we approach this differently than conventional solutions?
        Think outside the box."""
    )

    print("Innovator's Response:")
    print(result.final_output)
    print("\n" + "="*80 + "\n")


async def demonstrate_custom_training():
    """Demonstrate creating a custom training profile."""
    print("=== Custom Training Demonstration ===")

    # Create a custom training profile for a research assistant
    research_profile = TrainingProfile(
        name="Research Specialist",
        description="Specialized in academic research and knowledge synthesis",
        skill_domains={"problem_solving", "domain_expertise", "meta_cognition", "communication"},
        custom_instructions="""
        You specialize in academic research and knowledge synthesis. When working with research:
        - Always cite sources and acknowledge limitations
        - Look for methodological strengths and weaknesses
        - Identify gaps in current knowledge
        - Suggest future research directions
        - Present findings clearly for both experts and general audiences
        """
    )

    # Create agent with custom profile
    researcher = create_legendary_agent(
        name="Research Specialist",
        profile=research_profile
    )

    # Test research capabilities
    result = await Runner.run(
        researcher,
        """Synthesize current research on the effectiveness of mindfulness meditation for
        treating anxiety disorders. What does the evidence show, what are the limitations
        of existing studies, and what research gaps need to be addressed?"""
    )

    print("Researcher's Response:")
    print(result.final_output)
    print("\n" + "="*80 + "\n")


async def demonstrate_training_existing_agent():
    """Demonstrate applying training to an existing agent."""
    print("=== Training Existing Agent Demonstration ===")

    # Create a basic agent
    basic_agent = Agent(
        name="Basic Assistant",
        instructions="You are a helpful assistant."
    )

    # Apply legendary training to enhance it
    enhanced_agent = apply_legendary_training(
        basic_agent,
        get_training_profile("balanced_expert")
    )

    # Test the enhanced agent
    result = await Runner.run(
        enhanced_agent,
        """Help me think through a difficult decision: I've been offered a promotion that
        would significantly increase my salary and career prospects, but it would require
        relocating to a different country, away from family and friends. What framework
        could I use to make this decision thoughtfully?"""
    )

    print("Enhanced Agent's Response:")
    print(result.final_output)
    print("\n" + "="*80 + "\n")


async def main():
    """Run all demonstrations."""
    print("🚀 Legendary AI Training System Demonstration\n")
    print("This demo shows how legendary training transforms AI agents with master-level")
    print("capabilities across multiple domains of knowledge and skill.\n")

    demonstrations = [
        demonstrate_legendary_sage,
        demonstrate_analytical_master,
        demonstrate_communication_expert,
        demonstrate_innovation_genius,
        demonstrate_custom_training,
        demonstrate_training_existing_agent
    ]

    for demo in demonstrations:
        try:
            await demo()
        except Exception as e:
            print(f"Error in {demo.__name__}: {e}")
            print("Continuing with next demonstration...\n")

    print("🎯 Demonstration complete!")
    print("\nThe legendary training system enables creation of AI agents with:")
    print("- Deep expertise across multiple domains")
    print("- Sophisticated reasoning and problem-solving abilities")
    print("- Exceptional communication and interpersonal skills")
    print("- Strong ethical reasoning and moral decision-making")
    print("- Creative and innovative thinking capabilities")
    print("- Leadership and mentorship qualities")
    print("\nThese agents can tackle complex, multi-faceted challenges with the wisdom")
    print("and capabilities of legendary experts across human knowledge domains.")


if __name__ == "__main__":
    # Set your OpenAI API key in environment variables before running
    asyncio.run(main())
