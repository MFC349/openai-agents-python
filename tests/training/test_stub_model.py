"""Tests for the stub model implementation."""

import pytest

from agents import Runner
from agents.models.stub_model import StubModel, StubModelProvider
from agents.training import create_legendary_agent, get_training_profile


class TestStubModel:
    """Test stub model functionality."""

    def test_stub_model_initialization(self):
        """Test stub model initializes correctly."""
        model = StubModel("test-model")
        assert model.model_name == "test-model"
        assert isinstance(model.legendary_responses, dict)
        assert "legendary_sage" in model.legendary_responses
        assert "default" in model.legendary_responses

    @pytest.mark.asyncio
    async def test_stub_model_get_response(self):
        """Test stub model returns proper response."""
        model = StubModel()
        
        response = await model.get_response(
            system_instructions="Test legendary training",
            input="Test question",
            model_settings=None,
            tools=[],
            output_schema=None,
            handoffs=[],
            tracing=None,
            previous_response_id=None,
            conversation_id=None,
        )
        
        assert response.response_id is not None
        assert len(response.output) == 1
        assert response.output[0].role == "assistant"
        assert response.output[0].type == "message"
        assert len(response.output[0].content) == 1
        assert response.output[0].content[0].type == "output_text"
        assert len(response.output[0].content[0].text) > 0
        assert response.usage.requests == 1
        assert response.usage.output_tokens > 0

    @pytest.mark.asyncio
    async def test_stub_model_legendary_sage_response(self):
        """Test stub model provides legendary sage response for appropriate instructions."""
        model = StubModel()
        
        response = await model.get_response(
            system_instructions="You are a legendary sage with master-level capabilities across all domains",
            input="Solve a complex challenge",
            model_settings=None,
            tools=[],
            output_schema=None,
            handoffs=[],
            tracing=None,
            previous_response_id=None,
            conversation_id=None,
        )
        
        response_text = response.output[0].content[0].text
        assert "multi-domain analysis" in response_text.lower() or "strategic framework" in response_text.lower()

    @pytest.mark.asyncio
    async def test_stub_model_communication_expert_response(self):
        """Test stub model provides communication expert response."""
        model = StubModel()
        
        response = await model.get_response(
            system_instructions="You are a communication expert and master communicator",
            input="Explain something to different audiences",
            model_settings=None,
            tools=[],
            output_schema=None,
            handoffs=[],
            tracing=None,
            previous_response_id=None,
            conversation_id=None,
        )
        
        response_text = response.output[0].content[0].text
        assert "audience" in response_text.lower() and "explanation" in response_text.lower()

    @pytest.mark.asyncio
    async def test_stub_model_stream_response(self):
        """Test stub model streaming response."""
        model = StubModel()
        
        events = []
        async for event in model.stream_response(
            system_instructions="Test instructions",
            input="Test question", 
            model_settings=None,
            tools=[],
            output_schema=None,
            handoffs=[],
            tracing=None,
            previous_response_id=None,
            conversation_id=None,
        ):
            events.append(event)
        
        assert len(events) > 1  # Should have multiple streaming events
        assert events[-1]["type"] == "final"
        assert "response" in events[-1]


class TestStubModelProvider:
    """Test stub model provider."""

    def test_provider_initialization(self):
        """Test provider initializes correctly."""
        provider = StubModelProvider()
        assert provider.model is not None

    def test_provider_get_model(self):
        """Test provider returns stub model."""
        provider = StubModelProvider()
        model = provider.get_model("test-model")
        
        assert isinstance(model, StubModel)
        assert model.model_name == "test-model"

    def test_provider_get_model_none(self):
        """Test provider handles None model name."""
        provider = StubModelProvider()
        model = provider.get_model(None)
        
        assert isinstance(model, StubModel)
        assert model.model_name == "stub-legendary-model"


class TestStubModelIntegration:
    """Test stub model integration with legendary training system."""

    @pytest.mark.asyncio
    async def test_stub_model_with_legendary_agent(self):
        """Test stub model works with legendary agents."""
        # This test requires mocking the OpenAI provider to use stub model
        # For now, we'll test that the system can handle stub models conceptually
        
        profile = get_training_profile("communication_expert")
        agent = create_legendary_agent("Test Agent", profile)
        
        # Verify agent is created successfully
        assert agent.name == "Test Agent"
        assert "communication" in agent.instructions.lower()

    def test_stub_model_response_mapping(self):
        """Test that stub model maps system instructions to appropriate responses."""
        model = StubModel()
        
        # Test different instruction patterns
        test_cases = [
            ("legendary sage", "legendary_sage"),
            ("analytical master", "analytical_master"), 
            ("communication expert", "communication_expert"),
            ("innovation genius", "innovation_genius"),
            ("random instructions", "default")
        ]
        
        for instructions, expected_response_key in test_cases:
            response_text = model._generate_response(instructions, "test input")
            
            if expected_response_key == "default":
                assert "systematic thinking" in response_text
            else:
                expected_content = model.legendary_responses[expected_response_key]
                # Should use the specific response for that profile
                assert response_text == expected_content

    def test_stub_model_handles_various_inputs(self):
        """Test stub model handles different input formats."""
        model = StubModel()
        
        # Test string input
        text_response = model._generate_response("test instructions", "string input")
        assert isinstance(text_response, str)
        assert len(text_response) > 0
        
        # Test empty input
        empty_response = model._generate_response("test instructions", "")
        assert isinstance(empty_response, str)
        assert len(empty_response) > 0