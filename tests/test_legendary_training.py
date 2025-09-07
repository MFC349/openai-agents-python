"""Tests for the legendary training system."""

import pytest

from agents import Agent
from agents.training import (
    LegendaryTraining,
    TrainingFocus,
    TrainingIntensity,
    TrainingProfile,
    apply_legendary_training,
    create_legendary_agent,
    get_training_profile,
)
from agents.training.skill_domains import SKILL_DOMAINS


class TestSkillDomains:
    """Test skill domain functionality."""

    def test_all_skill_domains_have_required_methods(self):
        """Test that all skill domains implement required methods."""
        for _domain_name, domain in SKILL_DOMAINS.items():
            assert hasattr(domain, 'get_instructions')
            assert hasattr(domain, 'get_prompts')
            assert callable(domain.get_instructions)
            assert callable(domain.get_prompts)

            # Test methods return expected types
            instructions = domain.get_instructions()
            prompts = domain.get_prompts()

            assert isinstance(instructions, str)
            assert len(instructions) > 0
            assert isinstance(prompts, list)
            assert len(prompts) > 0
            assert all(isinstance(prompt, str) for prompt in prompts)

    def test_skill_domains_have_content(self):
        """Test that skill domains have meaningful content."""
        for _domain_name, domain in SKILL_DOMAINS.items():
            assert len(domain.name) > 0
            assert len(domain.description) > 0
            assert len(domain.core_principles) > 0
            assert len(domain.techniques) > 0

            # Instructions should mention the domain
            instructions = domain.get_instructions()
            assert len(instructions) > 100  # Should be substantial

            # Prompts should be meaningful
            prompts = domain.get_prompts()
            assert len(prompts) >= 3  # Should have multiple examples


class TestTrainingProfile:
    """Test training profile functionality."""

    def test_training_profile_creation(self):
        """Test creating a training profile."""
        profile = TrainingProfile(
            name="Test Profile",
            description="Test description",
            skill_domains={"problem_solving", "communication"}
        )

        assert profile.name == "Test Profile"
        assert profile.description == "Test description"
        assert profile.skill_domains == {"problem_solving", "communication"}
        assert profile.intensity == TrainingIntensity.ADVANCED  # default
        assert profile.focus == TrainingFocus.COMPREHENSIVE  # default

    def test_get_skill_objects(self):
        """Test getting skill objects from profile."""
        profile = TrainingProfile(
            name="Test",
            description="Test",
            skill_domains={"problem_solving", "communication", "invalid_domain"}
        )

        skill_objects = profile.get_skill_objects()
        assert len(skill_objects) == 2  # Only valid domains
        assert all(hasattr(obj, 'get_instructions') for obj in skill_objects)


class TestLegendaryTraining:
    """Test legendary training system."""

    def test_training_system_initialization(self):
        """Test training system initializes correctly."""
        training = LegendaryTraining()

        assert len(training.base_instructions) > 0
        assert len(training.legendary_principles) > 0
        assert isinstance(training.legendary_principles, list)

    def test_generate_instructions(self):
        """Test instruction generation."""
        training = LegendaryTraining()
        profile = TrainingProfile(
            name="Test",
            description="Test",
            skill_domains={"problem_solving"},
            intensity=TrainingIntensity.LEGENDARY,
            focus=TrainingFocus.ANALYTICAL
        )

        instructions = training.generate_instructions(profile)

        assert isinstance(instructions, str)
        assert len(instructions) > 1000  # Should be comprehensive
        assert "legendary" in instructions.lower()
        assert "problem" in instructions.lower()
        assert "analytical" in instructions.lower()

    def test_custom_instructions_included(self):
        """Test that custom instructions are included."""
        training = LegendaryTraining()
        custom_text = "This is custom training content."
        profile = TrainingProfile(
            name="Test",
            description="Test",
            skill_domains={"communication"},
            custom_instructions=custom_text
        )

        instructions = training.generate_instructions(profile)
        assert custom_text in instructions


class TestPredefinedProfiles:
    """Test predefined training profiles."""

    def test_all_predefined_profiles_exist(self):
        """Test that all expected predefined profiles exist."""
        expected_profiles = [
            "legendary_sage",
            "analytical_master",
            "communication_expert",
            "innovation_genius",
            "ethical_leader",
            "balanced_expert"
        ]

        for profile_name in expected_profiles:
            profile = get_training_profile(profile_name)
            assert isinstance(profile, TrainingProfile)
            assert len(profile.name) > 0
            assert len(profile.description) > 0
            assert len(profile.skill_domains) > 0

    def test_legendary_sage_is_comprehensive(self):
        """Test that legendary sage includes all skill domains."""
        sage_profile = get_training_profile("legendary_sage")

        assert sage_profile.intensity == TrainingIntensity.LEGENDARY
        assert sage_profile.focus == TrainingFocus.COMPREHENSIVE
        assert len(sage_profile.skill_domains) == len(SKILL_DOMAINS)
        assert sage_profile.skill_domains == set(SKILL_DOMAINS.keys())

    def test_specialized_profiles_have_focused_skills(self):
        """Test that specialized profiles have appropriate skill focus."""
        analytical = get_training_profile("analytical_master")
        assert "problem_solving" in analytical.skill_domains
        assert analytical.focus == TrainingFocus.ANALYTICAL

        communicator = get_training_profile("communication_expert")
        assert "communication" in communicator.skill_domains
        assert communicator.focus == TrainingFocus.INTERPERSONAL

        innovator = get_training_profile("innovation_genius")
        assert "creative_thinking" in innovator.skill_domains
        assert innovator.focus == TrainingFocus.CREATIVE

    def test_invalid_profile_raises_error(self):
        """Test that invalid profile name raises ValueError."""
        with pytest.raises(ValueError, match="Unknown profile"):
            get_training_profile("invalid_profile_name")


class TestAgentCreation:
    """Test agent creation and enhancement."""

    def test_create_legendary_agent(self):
        """Test creating a new legendary agent."""
        profile = get_training_profile("balanced_expert")
        agent = create_legendary_agent(
            name="Test Agent",
            profile=profile
        )

        assert isinstance(agent, Agent)
        assert agent.name == "Test Agent"
        assert len(agent.instructions) > 1000  # Should be comprehensive
        assert "legendary" in agent.instructions.lower()

    def test_create_agent_with_base_instructions(self):
        """Test creating agent with base instructions."""
        profile = get_training_profile("communication_expert")
        base_instructions = "You are a customer service agent."

        agent = create_legendary_agent(
            name="CS Agent",
            profile=profile,
            base_instructions=base_instructions
        )

        assert base_instructions in agent.instructions
        assert "communication" in agent.instructions.lower()

    def test_apply_training_to_existing_agent(self):
        """Test applying training to an existing agent."""
        # Create basic agent
        basic_agent = Agent(
            name="Basic Agent",
            instructions="You are helpful."
        )

        original_instructions = basic_agent.instructions

        # Apply training
        profile = get_training_profile("ethical_leader")
        enhanced_agent = apply_legendary_training(basic_agent, profile)

        # Verify enhancement
        assert enhanced_agent is basic_agent  # Same object
        assert original_instructions in enhanced_agent.instructions
        assert "ethical" in enhanced_agent.instructions.lower()
        assert len(enhanced_agent.instructions) > len(original_instructions)

    def test_agent_with_custom_model(self):
        """Test creating agent with custom model."""
        profile = get_training_profile("analytical_master")
        agent = create_legendary_agent(
            name="Custom Model Agent",
            profile=profile,
            model="gpt-4"
        )

        assert agent.model == "gpt-4"

    def test_agent_retains_other_properties(self):
        """Test that agent retains other properties during training."""
        basic_agent = Agent(
            name="Test Agent",
            instructions="Basic instructions",
            model="gpt-4"
        )

        original_model = basic_agent.model

        # Apply training
        profile = get_training_profile("innovation_genius")
        enhanced_agent = apply_legendary_training(basic_agent, profile)

        # Verify properties retained
        assert enhanced_agent.model == original_model
        assert enhanced_agent.name == "Test Agent"


class TestTrainingIntegration:
    """Test integration with the broader agent system."""

    def test_training_preserves_agent_interface(self):
        """Test that trained agents maintain the standard Agent interface."""
        profile = get_training_profile("legendary_sage")
        agent = create_legendary_agent("Test", profile)

        # Should have all standard Agent attributes
        assert hasattr(agent, 'name')
        assert hasattr(agent, 'instructions')
        assert hasattr(agent, 'model')
        assert hasattr(agent, 'tools')
        assert hasattr(agent, 'handoffs')

    def test_multiple_training_applications(self):
        """Test applying training multiple times."""
        agent = Agent(name="Multi-trained", instructions="Base instructions")

        # Apply different training profiles
        profile1 = get_training_profile("communication_expert")
        profile2 = get_training_profile("analytical_master")

        agent = apply_legendary_training(agent, profile1)
        first_length = len(agent.instructions)

        agent = apply_legendary_training(agent, profile2)
        second_length = len(agent.instructions)

        # Instructions should accumulate
        assert second_length > first_length
        assert "communication" in agent.instructions.lower()
        assert "analytical" in agent.instructions.lower()
