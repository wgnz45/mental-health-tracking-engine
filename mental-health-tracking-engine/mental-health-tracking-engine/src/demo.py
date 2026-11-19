from .models import LongitudinalEmotionalState, SafetyAssessment
from .safety import transition_safety_state


def main() -> None:
    state = LongitudinalEmotionalState(user_id="synthetic-user-001")
    assessment = SafetyAssessment(
        user_id="synthetic-user-001", session_id="synthetic-session-001",
        current_suicidal_thoughts=True, current_intent=False,
        current_plan=False, safety_check_started=True,
    )
    print(transition_safety_state(state, assessment).model_dump_json(indent=2))


if __name__ == "__main__":
    main()
