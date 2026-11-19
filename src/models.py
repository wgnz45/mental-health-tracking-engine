from __future__ import annotations
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class InformationSource(str, Enum):
    USER_REPORTED = "user_reported"
    MODEL_INFERRED = "model_inferred"
    CLINICIAN_VERIFIED = "clinician_verified"


class ConfidenceLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RiskState(str, Enum):
    ROUTINE = "routine"
    CLARIFICATION_REQUIRED = "clarification_required"
    URGENT_HUMAN_REVIEW = "urgent_human_review"
    IMMEDIATE_EMERGENCY_RESPONSE = "immediate_emergency_response"


class EmotionalObservation(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    observation_id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    session_id: str
    observed_at: datetime = Field(default_factory=utc_now)
    category: str
    value: str
    source: InformationSource
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    evidence_message_id: Optional[str] = None
    context: Optional[str] = None


class SafetyAssessment(BaseModel):
    assessment_id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    session_id: str
    assessed_at: datetime = Field(default_factory=utc_now)
    current_suicidal_thoughts: Optional[bool] = None
    current_intent: Optional[bool] = None
    current_plan: Optional[bool] = None
    access_to_means: Optional[bool] = None
    current_attempt_or_injury: Optional[bool] = None
    immediate_danger_reported: Optional[bool] = None
    thoughts_or_plan_past_month: Optional[bool] = None
    self_harm_past_year: Optional[bool] = None
    hopelessness_reported: bool = False
    acute_distress_reported: bool = False
    safety_check_started: bool = False
    evidence_message_ids: list[str] = Field(default_factory=list)


class StateTransition(BaseModel):
    transition_id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    previous_state: RiskState
    new_state: RiskState
    reason: str
    assessment_id: str
    timestamp: datetime = Field(default_factory=utc_now)
    authorized_reviewer_id: Optional[str] = None


class LongitudinalEmotionalState(BaseModel):
    user_id: str
    observations: list[EmotionalObservation] = Field(default_factory=list)
    current_risk_state: RiskState = RiskState.ROUTINE
    transitions: list[StateTransition] = Field(default_factory=list)
    last_updated: datetime = Field(default_factory=utc_now)
