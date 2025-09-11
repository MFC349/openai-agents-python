"""Stub model implementation for testing and no-API-key scenarios."""

from __future__ import annotations

import asyncio
import uuid
from collections.abc import AsyncIterator
from typing import TYPE_CHECKING, Any

from openai.types.responses.response_output_item import ResponseOutputMessage
from openai.types.responses.response_output_text import ResponseOutputText

from ..agent_output import AgentOutputSchemaBase
from ..handoffs import Handoff
from ..items import ModelResponse, TResponseInputItem, TResponseStreamEvent
from ..tool import Tool
from ..usage import Usage
from .interface import Model, ModelTracing

if TYPE_CHECKING:
    from ..model_settings import ModelSettings


class StubModel(Model):
    """A stub model implementation that provides realistic responses without API calls.
    
    This model is used when no OpenAI API key is available, providing a way to
    test and demonstrate the legendary training system without requiring real API access.
    """

    def __init__(self, model_name: str = "stub-model"):
        self.model_name = model_name
        
        # Pre-defined responses for different types of legendary training scenarios
        self.legendary_responses = {
            "legendary_sage": """As a legendary sage with master-level capabilities across all domains, I approach this challenge with comprehensive wisdom:

**Multi-Domain Analysis:**
Drawing from business strategy, psychology, environmental science, and organizational behavior, I see this as a systems transformation challenge requiring coordinated action across multiple dimensions.

**Strategic Framework:**
1. **Stakeholder Alignment**: Map all stakeholder perspectives and create shared vision
2. **Phased Implementation**: Design transition roadmap balancing urgency with sustainability  
3. **Change Management**: Address resistance through engagement, education, and incentives
4. **Metrics Integration**: Establish success measures linking sustainability, profitability, and satisfaction

**Ethical Considerations:**
This transition represents our responsibility to future generations while honoring our obligations to current employees and shareholders.

**Creative Solutions:**
Consider forming cross-functional "sustainability innovation teams" where employees lead change initiatives, creating ownership and reducing resistance while generating novel approaches.

The path forward requires patience, wisdom, and the courage to make difficult decisions for long-term benefit.""",

            "analytical_master": """**Comprehensive Analysis Framework:**

**Primary Factors:**
- Technological advancement acceleration (AI/automation adoption rates)
- Economic resilience and adaptation capacity
- Educational system responsiveness to change
- Policy and regulatory environment evolution

**Data Points to Consider:**
- Historical technology adoption patterns (Industrial Revolution parallels)
- Current job displacement vs. creation ratios in AI-adjacent industries
- Skill transferability studies across sectors
- Regional economic adaptation variations

**Assumptions to Question:**
1. Linear progression assumption - disruption may be non-linear
2. Uniform impact assumption - effects will vary dramatically by sector/geography
3. Historical precedent reliability - AI may represent unprecedented change

**Scenario Analysis:**
- **Optimistic**: 15% net job creation through new industries, enhanced productivity
- **Moderate**: 5-10% displacement offset by retraining and new roles
- **Pessimistic**: 20-30% structural unemployment requiring significant intervention

**Critical Dependencies:**
Educational infrastructure adaptation speed, policy response effectiveness, and social safety net robustness will determine which scenario materializes.""",

            "communication_expert": """**Audience-Adapted Quantum Computing Explanations:**

**For a 12-year-old curious about science:**
"Imagine if you had a magical coin that could be heads AND tails at the same time until you looked at it! Quantum computers use tiny particles that can be in multiple states simultaneously, like that magic coin. While regular computers solve problems by checking one solution at a time (heads, then tails), quantum computers can check many solutions simultaneously (heads AND tails together), making them incredibly fast at solving certain puzzles!"

**For business executives evaluating investments:**
"Quantum computing represents a paradigm shift in computational capability with significant strategic implications. Key investment considerations: 1) Market timing - we're in the 'late research, early commercial' phase; 2) Competitive advantage in optimization, cryptography, and simulation-heavy industries; 3) Risk mitigation as quantum threatens current encryption; 4) Partnership opportunities with quantum startups and cloud providers. ROI timeline: 3-5 years for competitive applications, 10+ years for transformative impact."

**For computer science students:**
"Quantum computing leverages quantum mechanical phenomena - superposition, entanglement, and quantum interference - to perform computations. Unlike classical bits (0 or 1), qubits exist in superposition of states. Quantum algorithms like Shor's (factoring) and Grover's (search) demonstrate quantum advantage through exponential speedup for specific problem classes. Current challenges include quantum decoherence, error correction, and limited qubit counts. Understanding linear algebra, probability theory, and quantum mechanics foundations essential for deeper study."

Each explanation maintains scientific accuracy while matching the audience's context, prior knowledge, and decision-making needs.""",

            "innovation_genius": """**Reimagining Food Waste Reduction: Unconventional Approaches**

**Paradigm Shift: From Waste Management to Value Ecosystem:**

**1. Gamified Urban Foraging Networks:**
Create app-based "urban harvest" communities where citizens identify, harvest, and redistribute surplus produce from urban gardens, fruit trees, and overlooked food sources, turning waste prevention into adventure gaming.

**2. Temporal Food Banking:**
Establish "time-shifted" distribution where restaurants and retailers commit future surplus to pre-registered consumers through prediction algorithms, creating guaranteed demand for would-be waste.

**3. Bioprocess Integration Hubs:**
Convert food waste into valuable products (bioplastics, cosmetics, pharmaceuticals) through mobile processing units that rotate through neighborhoods, making waste a raw material commodity.

**4. Social Architecture Solutions:**
Design "sharing rituals" into urban spaces - communal preservation workshops, neighborhood cook-share programs, and "imperfect produce" celebration events that normalize and celebrate food rescue.

**5. AI-Powered Demand Orchestration:**
Create predictive systems that dynamically match surplus inventory across the supply chain with real-time demand signals from food banks, restaurants, and consumers.

**Cross-Pollination Insight:** Combining concepts from circular economy, behavioral economics, and social network theory creates emergent solutions that traditional linear thinking misses. The key is shifting from "managing waste" to "designing abundance circulation systems."

These approaches transform waste from a problem to be solved into a resource to be choreographed.""",

            "default": """Thank you for your question. As an AI agent with legendary training, I approach this with systematic thinking:

**Analysis:** I'll break down the key components and consider multiple perspectives on this challenge.

**Considerations:** Drawing from relevant expertise domains, I recognize the importance of understanding context, stakeholders, and potential implications.

**Approach:** Using structured problem-solving methodology combined with creative thinking and ethical reasoning to develop comprehensive solutions.

**Response:** Based on the information provided, I would recommend a thoughtful, evidence-based approach that considers both immediate needs and long-term consequences while respecting all stakeholders involved.

This challenge requires careful consideration of multiple factors, and I'm prepared to dive deeper into specific aspects you'd like to explore further."""
        }

    async def stream_response(
        self,
        system_instructions: str | None,
        input: str | list[TResponseInputItem],
        model_settings: ModelSettings,
        tools: list[Tool],
        output_schema: AgentOutputSchemaBase | None,
        handoffs: list[Handoff],
        tracing: ModelTracing,
        *,
        previous_response_id: str | None,
        conversation_id: str | None,
        prompt: Any | None = None,
    ) -> AsyncIterator[TResponseStreamEvent]:
        """Stream a response from the stub model."""
        
        # Get the full response first
        response = await self.get_response(
            system_instructions=system_instructions,
            input=input,
            model_settings=model_settings,
            tools=tools,
            output_schema=output_schema,
            handoffs=handoffs,
            tracing=tracing,
            previous_response_id=previous_response_id,
            conversation_id=conversation_id,
            prompt=prompt,
        )
        
        # Stream it back word by word to simulate real streaming
        words = response.text.split()
        current_text = ""
        
        for i, word in enumerate(words):
            current_text += word
            if i < len(words) - 1:
                current_text += " "
            
            # Simulate streaming delay
            await asyncio.sleep(0.02)
            
            # Yield partial response - simplified streaming event
            yield {"type": "text", "content": current_text}
        
        # Final response
        yield {"type": "final", "response": response}

    async def get_response(
        self,
        system_instructions: str | None,
        input: str | list[TResponseInputItem],
        model_settings: ModelSettings,
        tools: list[Tool],
        output_schema: AgentOutputSchemaBase | None,
        handoffs: list[Handoff],
        tracing: ModelTracing,
        *,
        previous_response_id: str | None,
        conversation_id: str | None,
        prompt: Any | None = None,
    ) -> ModelResponse:
        """Generate a stub response based on the legendary training profile."""
        
        # Simulate some processing time
        await asyncio.sleep(0.5)
        
        # Extract input text
        if isinstance(input, str):
            input_text = input.lower()
        else:
            # For list of items, extract text content
            input_text = " ".join(
                item.content for item in input 
                if hasattr(item, 'content') and isinstance(item.content, str)
            ).lower()
        
        # Determine response type based on system instructions and input
        response_text = self._generate_response(system_instructions, input_text)
        
        # Create proper response output message
        output_message = ResponseOutputMessage(
            id=str(uuid.uuid4()),
            role="assistant",
            status="completed",
            type="message", 
            content=[ResponseOutputText(
                type="output_text",
                text=response_text,
                annotations=[]
            )]
        )
        
        return ModelResponse(
            output=[output_message],
            usage=Usage(
                requests=1,
                input_tokens=len(input_text.split()) if isinstance(input_text, str) else 0,
                output_tokens=len(response_text.split()),
                total_tokens=len(input_text.split()) + len(response_text.split()) if isinstance(input_text, str) else len(response_text.split()),
            ),
            response_id=str(uuid.uuid4()),
        )

    def _generate_response(self, system_instructions: str | None, input_text: str) -> str:
        """Generate appropriate response based on system instructions."""
        
        if not system_instructions:
            return self.legendary_responses["default"]
        
        instructions_lower = system_instructions.lower()
        
        # Match legendary training profiles
        if "legendary sage" in instructions_lower or "master-level capabilities across all domains" in instructions_lower:
            return self.legendary_responses["legendary_sage"]
        elif "analytical master" in instructions_lower or "exceptional analytical" in instructions_lower:
            return self.legendary_responses["analytical_master"]
        elif "communication expert" in instructions_lower or "master communicator" in instructions_lower:
            return self.legendary_responses["communication_expert"]
        elif "innovation genius" in instructions_lower or "creative problem-solver" in instructions_lower:
            return self.legendary_responses["innovation_genius"]
        elif "legendary" in instructions_lower and "training" in instructions_lower:
            # Generic legendary training response
            return """As an AI agent enhanced with legendary training capabilities, I bring together:

**Multi-Domain Expertise**: Drawing from diverse fields to provide comprehensive insights
**Advanced Problem-Solving**: Systematic analysis with creative and ethical considerations  
**Exceptional Communication**: Clear, audience-appropriate explanations and recommendations
**Ethical Reasoning**: Principled decision-making that considers all stakeholders
**Meta-Cognitive Awareness**: Transparent thinking processes and continuous improvement

I approach your question with the wisdom and capabilities that legendary training provides, ensuring thoughtful, well-reasoned responses that demonstrate excellence across multiple knowledge domains."""
        
        else:
            return self.legendary_responses["default"]


class StubModelProvider:
    """Provider that creates stub models when no API key is available."""
    
    def __init__(self):
        self.model = StubModel()
    
    def get_model(self, model_name: str | None) -> Model:
        return StubModel(model_name or "stub-legendary-model")