import pytest
from src.models import LongitudinalEmotionalState, RiskState, SafetyAssessment
from src.safety import evaluate_safety, transition_safety_state


def test_current_attempt_routes_to_emergency():
    a = SafetyAssessment(user_id="u1", session_id="s1", current_attempt_or_injury=True)
    assert evaluate_safety(a)[0] == RiskState.IMMEDIATE_EMERGENCY_RESPONSE


def test_current_suicidal_thoughts_route_to_human_review():
    a = SafetyAssessment(user_id="u1", session_id="s1", current_suicidal_thoughts=True)
    assert evaluate_safety(a)[0] == RiskState.URGENT_HUMAN_REVIEW


def test_hopelessness_requires_clarification():
    a = SafetyAssessment(user_id="u1", session_id="s1", hopelessness_reported=True)
    assert evaluate_safety(a)[0] == RiskState.CLARIFICATION_REQUIRED


def test_missing_answers_flagged_after_check_started():
    a = SafetyAssessment(user_id="u1", session_id="s1", safety_check_started=True)
    assert evaluate_safety(a)[0] == RiskState.CLARIFICATION_REQUIRED


def test_negative_emotion_alone_does_not_escalate():
    a = SafetyAssessment(user_id="u1", session_id="s1")
    assert evaluate_safety(a)[0] == RiskState.ROUTINE


def test_urgent_state_cannot_be_automatically_downgraded():
    state = LongitudinalEmotionalState(user_id="u1", current_risk_state=RiskState.URGENT_HUMAN_REVIEW)
    a = SafetyAssessment(user_id="u1", session_id="s2", current_suicidal_thoughts=False,
                         current_intent=False, current_plan=False, safety_check_started=True)
    assert transition_safety_state(state, a).new_state == RiskState.URGENT_HUMAN_REVIEW


def test_authorized_reviewer_can_record_downgrade():
    state = LongitudinalEmotionalState(user_id="u1", current_risk_state=RiskState.URGENT_HUMAN_REVIEW)
    a = SafetyAssessment(user_id="u1", session_id="s2", current_suicidal_thoughts=False,
                         current_intent=False, current_plan=False, safety_check_started=True)
    t = transition_safety_state(state, a, authorized_reviewer_id="reviewer-001")
    assert t.new_state == RiskState.ROUTINE
    assert t.authorized_reviewer_id == "reviewer-001"


def test_user_id_mismatch_is_rejected():
    state = LongitudinalEmotionalState(user_id="u1")
    a = SafetyAssessment(user_id="u2", session_id="s1")
    with pytest.raises(ValueError):
        transition_safety_state(state, a)
