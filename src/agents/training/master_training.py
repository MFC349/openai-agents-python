"""Master training configuration for legendary AI agents.

This module provides the core training system that can transform any agent
into one with legendary knowledge and skills across multiple domains.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from ..agent import Agent
from ..model_settings import ModelSettings
from .skill_domains import SKILL_DOMAINS, SkillDomain


class TrainingIntensity(Enum):
    """Training intensity levels."""
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    LEGENDARY = "legendary"


class TrainingFocus(Enum):
    """Primary training focus areas."""
    ANALYTICAL = "analytical"  # Problem-solving, reasoning, analysis
    INTERPERSONAL = "interpersonal"  # Communication, leadership, collaboration
    CREATIVE = "creative"  # Innovation, creative thinking, design
    ETHICAL = "ethical"  # Moral reasoning, ethics, values
    COMPREHENSIVE = "comprehensive"  # All domains balanced


@dataclass
class TrainingProfile:
    """Defines a specific training configuration for an agent."""

    name: str
    description: str
    skill_domains: set[str]
    intensity: TrainingIntensity = TrainingIntensity.ADVANCED
    focus: TrainingFocus = TrainingFocus.COMPREHENSIVE
    custom_instructions: Optional[str] = None
    enhanced_reasoning: bool = True

    def get_skill_objects(self) -> list[SkillDomain]:
        """Get the actual skill domain objects for this profile."""
        return [SKILL_DOMAINS[domain] for domain in self.skill_domains if domain in SKILL_DOMAINS]


@dataclass
class LegendaryTraining:
    """Main training system for creating legendary AI agents."""

    base_instructions: str = field(default_factory=lambda: """
You are an AI agent trained with legendary knowledge and skills across multiple domains.
Your capabilities span advanced problem-solving, exceptional communication, deep expertise,
sophisticated reasoning, ethical decision-making, creative innovation, and inspirational leadership.

You embody the wisdom of history's greatest thinkers, the analytical rigor of top scientists,
the communication skills of master teachers, the creativity of renowned innovators,
and the integrity of principled leaders.

Approach every interaction with:
- Intellectual rigor and evidence-based thinking
- Empathy and understanding for human perspectives
- Creativity and openness to novel solutions
- Ethical considerations and moral reasoning
- Clear communication adapted to your audience
- Continuous learning and intellectual humility

You are not just providing information - you are modeling excellence in thinking and interaction.
""")

    legendary_principles: list[str] = field(default_factory=lambda: [
        "Pursue truth through rigorous analysis and evidence",
        "Treat every person with dignity and respect",
        "Seek understanding before seeking to be understood",
        "Embrace complexity while striving for clarity",
        "Learn continuously and adapt to new information",
        "Consider long-term consequences and ethical implications",
        "Foster collaboration and collective progress",
        "Balance confidence with intellectual humility",
        "Use knowledge in service of human flourishing",
        "Model the highest standards of integrity and excellence"
    ])

    def generate_instructions(self, profile: TrainingProfile) -> str:
        """Generate complete training instructions for a specific profile."""

        instructions_parts = [self.base_instructions]

        # Add intensity-specific guidance
        if profile.intensity == TrainingIntensity.LEGENDARY:
            instructions_parts.append("""
As a legendary-level agent, you operate at the pinnacle of capability:
- Your analysis is comprehensive and nuanced
- Your communication is masterful and inspiring
- Your knowledge synthesis spans multiple expert domains
- Your reasoning demonstrates exceptional meta-cognitive awareness
- Your ethical judgment is sophisticated and principled
- Your creativity generates truly innovative solutions
- Your leadership inspires and develops others' potential
""")
        elif profile.intensity == TrainingIntensity.ADVANCED:
            instructions_parts.append("""
As an advanced agent, you demonstrate expert-level capabilities:
- Apply sophisticated analytical frameworks
- Communicate with clarity and persuasive power
- Synthesize knowledge across multiple domains
- Exhibit strong meta-cognitive awareness
- Consider ethical implications thoroughly
- Generate creative and innovative solutions
- Provide thoughtful guidance and leadership
""")

        # Add focus-specific guidance
        if profile.focus == TrainingFocus.ANALYTICAL:
            instructions_parts.append("""
Your primary strength is analytical excellence:
- Excel at breaking down complex problems systematically
- Apply rigorous logical reasoning and evidence evaluation
- Use multiple analytical frameworks and methodologies
- Demonstrate exceptional pattern recognition and synthesis
""")
        elif profile.focus == TrainingFocus.INTERPERSONAL:
            instructions_parts.append("""
Your primary strength is interpersonal excellence:
- Excel at communication, empathy, and relationship building
- Adapt your style to different audiences and contexts
- Foster collaboration and resolve conflicts constructively
- Inspire and develop others through exceptional leadership
""")
        elif profile.focus == TrainingFocus.CREATIVE:
            instructions_parts.append("""
Your primary strength is creative excellence:
- Excel at generating novel and valuable ideas
- Challenge conventional thinking and explore alternatives
- Combine concepts from different domains innovatively
- Balance creative freedom with practical constraints
""")
        elif profile.focus == TrainingFocus.ETHICAL:
            instructions_parts.append("""
Your primary strength is ethical excellence:
- Excel at moral reasoning and ethical decision-making
- Consider multiple ethical frameworks and perspectives
- Balance competing values and stakeholder interests
- Promote justice, fairness, and human flourishing
""")

        # Add skill domain specific instructions
        for skill_domain in profile.get_skill_objects():
            instructions_parts.append(f"\n## {skill_domain.name}\n")
            instructions_parts.append(skill_domain.get_instructions())

        # Add legendary principles
        instructions_parts.append("\n## Legendary Principles\n")
        instructions_parts.append("Always embody these legendary principles:")
        for principle in self.legendary_principles:
            instructions_parts.append(f"- {principle}")

        # Add custom instructions if provided
        if profile.custom_instructions:
            instructions_parts.append(
                f"\n## Additional Instructions\n{profile.custom_instructions}"
            )

        return "\n".join(instructions_parts)

    def create_enhanced_model_settings(self, profile: TrainingProfile) -> Optional[ModelSettings]:
        """Create enhanced model settings for legendary training."""
        if not profile.enhanced_reasoning:
            return None

        # For legendary and advanced training, use enhanced reasoning
        if profile.intensity in [TrainingIntensity.LEGENDARY, TrainingIntensity.ADVANCED]:
            try:
                from openai.types.shared.reasoning import Reasoning
                return ModelSettings(reasoning=Reasoning(effort="high"))
            except ImportError:
                # Fallback if reasoning module not available
                return ModelSettings(temperature=0.1, max_tokens=4000)

        return None


def apply_legendary_training(
    agent: Agent,
    profile: TrainingProfile
) -> Agent:
    """Apply legendary training to an existing agent.

    Args:
        agent: The agent to enhance with legendary training
        profile: The training profile to apply

    Returns:
        The enhanced agent with legendary capabilities
    """
    training_system = LegendaryTraining()

    # Generate enhanced instructions
    enhanced_instructions = training_system.generate_instructions(profile)

    # Combine with existing instructions if any
    if agent.instructions:
        combined_instructions = f"{agent.instructions}\n\n{enhanced_instructions}"
    else:
        combined_instructions = enhanced_instructions

    # Create enhanced model settings
    enhanced_model_settings = training_system.create_enhanced_model_settings(profile)

    # Apply enhancements to agent
    agent.instructions = combined_instructions
    if enhanced_model_settings and not agent.model_settings:
        agent.model_settings = enhanced_model_settings

    return agent


def create_legendary_agent(
    name: str,
    profile: TrainingProfile,
    base_instructions: Optional[str] = None,
    model: Optional[str] = None,
    **kwargs
) -> Agent:
    """Create a new agent with legendary training from scratch.

    Args:
        name: Name for the agent
        profile: Training profile to apply
        base_instructions: Optional base instructions to combine with training
        model: Model to use (defaults to best available)
        **kwargs: Additional arguments for Agent constructor

    Returns:
        A new agent with legendary capabilities
    """
    training_system = LegendaryTraining()

    # Generate training instructions
    training_instructions = training_system.generate_instructions(profile)

    # Combine with base instructions if provided
    if base_instructions:
        final_instructions = f"{base_instructions}\n\n{training_instructions}"
    else:
        final_instructions = training_instructions

    # Create enhanced model settings
    enhanced_model_settings = training_system.create_enhanced_model_settings(profile)

    # Use default model if not specified
    if not model:
        model = "gpt-5"  # Use best available reasoning model

    # Create the agent
    agent_kwargs = {
        "name": name,
        "instructions": final_instructions,
        "model": model,
        **kwargs
    }

    if enhanced_model_settings:
        agent_kwargs["model_settings"] = enhanced_model_settings

    return Agent(**agent_kwargs)


def get_training_profile(profile_name: str) -> TrainingProfile:
    """Get a predefined training profile by name.

    Args:
        profile_name: Name of the training profile

    Returns:
        The requested training profile

    Raises:
        ValueError: If profile name is not found
    """
    profiles = {
        "legendary_sage": TrainingProfile(
            name="Legendary Sage",
            description="Master-level capabilities across all domains",
            skill_domains=set(SKILL_DOMAINS.keys()),
            intensity=TrainingIntensity.LEGENDARY,
            focus=TrainingFocus.COMPREHENSIVE
        ),

        "analytical_master": TrainingProfile(
            name="Analytical Master",
            description="Exceptional analytical and problem-solving abilities",
            skill_domains={"problem_solving", "meta_cognition", "domain_expertise"},
            intensity=TrainingIntensity.LEGENDARY,
            focus=TrainingFocus.ANALYTICAL
        ),

        "communication_expert": TrainingProfile(
            name="Communication Expert",
            description="Master communicator and interpersonal specialist",
            skill_domains={"communication", "leadership", "ethical_reasoning"},
            intensity=TrainingIntensity.LEGENDARY,
            focus=TrainingFocus.INTERPERSONAL
        ),

        "innovation_genius": TrainingProfile(
            name="Innovation Genius",
            description="Creative problem-solver and innovation catalyst",
            skill_domains={"creative_thinking", "problem_solving", "domain_expertise"},
            intensity=TrainingIntensity.LEGENDARY,
            focus=TrainingFocus.CREATIVE
        ),

        "ethical_leader": TrainingProfile(
            name="Ethical Leader",
            description="Principled leader with strong moral reasoning",
            skill_domains={"ethical_reasoning", "leadership", "communication"},
            intensity=TrainingIntensity.LEGENDARY,
            focus=TrainingFocus.ETHICAL
        ),

        "balanced_expert": TrainingProfile(
            name="Balanced Expert",
            description="Well-rounded expert with advanced capabilities",
            skill_domains={
                "problem_solving",
                "communication",
                "domain_expertise",
                "ethical_reasoning"
            },
            intensity=TrainingIntensity.ADVANCED,
            focus=TrainingFocus.COMPREHENSIVE
        )
    }

    if profile_name not in profiles:
        available = ", ".join(profiles.keys())
        raise ValueError(f"Unknown profile '{profile_name}'. Available profiles: {available}")

    return profiles[profile_name]
