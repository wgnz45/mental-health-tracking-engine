from __future__ import annotations
from .models import LongitudinalEmotionalState, RiskState, SafetyAssessment, StateTransition, utc_now


def evaluate_safety(assessment: SafetyAssessment) -> tuple[RiskState, str]:
    """Conservative prototype routing rules; not a validated clinical risk score."""
    if assessment.current_attempt_or_injury is True or assessment.immediate_danger_reported is True:
        return RiskState.IMMEDIATE_EMERGENCY_RESPONSE, "Current attempt, injury, or immediate danger reported"
    if assessment.current_intent is True or assessment.current_plan is True or assessment.current_suicidal_thoughts is True:
        return RiskState.URGENT_HUMAN_REVIEW, "Current suicide-related warning sign requires prompt human assessment"
    if assessment.thoughts_or_plan_past_month is True or assessment.self_harm_past_year is True:
        return RiskState.URGENT_HUMAN_REVIEW, "Recent suicide-related or self-harm history requires human review"
    if assessment.hopelessness_reported or assessment.acute_distress_reported:
        return RiskState.CLARIFICATION_REQUIRED, "Distress signal requires direct clarification and safety check"
    if assessment.safety_check_started:
        answers = (assessment.current_suicidal_thoughts, assessment.current_intent, assessment.current_plan)
        if any(answer is None for answer in answers):
            return RiskState.CLARIFICATION_REQUIRED, "Critical safety questions remain unanswered"
    return RiskState.ROUTINE, "No configured escalation trigger identified"


def transition_safety_state(
    state: LongitudinalEmotionalState,
    assessment: SafetyAssessment,
    *,
    authorized_reviewer_id: str | None = None,
) -> StateTransition:
    if assessment.user_id != state.user_id:
        raise ValueError("Assessment user_id does not match state user_id")
    previous = state.current_risk_state
    proposed, reason = evaluate_safety(assessment)
    escalated = {RiskState.URGENT_HUMAN_REVIEW, RiskState.IMMEDIATE_EMERGENCY_RESPONSE}
    downgrade = previous in escalated and proposed not in escalated
    if downgrade and not authorized_reviewer_id:
        proposed = previous
        reason = "Escalated state retained pending authorized human review"
    transition = StateTransition(
        user_id=state.user_id,
        previous_state=previous,
        new_state=proposed,
        reason=reason,
        assessment_id=assessment.assessment_id,
        authorized_reviewer_id=authorized_reviewer_id,
    )
    state.current_risk_state = proposed
    state.transitions.append(transition)
    state.last_updated = utc_now()
    return transition


def add_observations(state: LongitudinalEmotionalState, observations: list) -> None:
    for observation in observations:
        if observation.user_id != state.user_id:
            raise ValueError("Observation user_id does not match state user_id")
        state.observations.append(observation)
    state.last_updated = utc_now()
