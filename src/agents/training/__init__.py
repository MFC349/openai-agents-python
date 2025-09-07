"""Training module for OpenAI Agents SDK.

This module provides comprehensive training configurations for AI agents,
implementing legendary knowledge and skills across multiple domains.
"""

from .master_training import (
    LegendaryTraining,
    TrainingFocus,
    TrainingIntensity,
    TrainingProfile,
    apply_legendary_training,
    create_legendary_agent,
    get_training_profile,
)
from .skill_domains import (
    CommunicationSkills,
    CreativeThinking,
    DomainExpertise,
    EthicalReasoning,
    LeadershipSkills,
    MetaCognition,
    ProblemSolving,
    SkillDomain,
)

__all__ = [
    "LegendaryTraining",
    "TrainingProfile",
    "TrainingIntensity",
    "TrainingFocus",
    "apply_legendary_training",
    "create_legendary_agent",
    "get_training_profile",
    "SkillDomain",
    "ProblemSolving",
    "CommunicationSkills",
    "DomainExpertise",
    "MetaCognition",
    "EthicalReasoning",
    "CreativeThinking",
    "LeadershipSkills",
]
