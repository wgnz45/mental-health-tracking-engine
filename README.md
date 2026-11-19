# Mental Health Tracking Engine (Prototype)

A small, privacy-conscious engineering prototype for storing user-reported emotional observations and routing safety-related signals to appropriate follow-up workflows.

**Status:** early prototype / not clinically validated. It is not a diagnostic tool, treatment system, crisis service, or substitute for qualified professionals.

## Scope

- Pydantic v2 schemas distinguish user-reported, model-inferred, and clinician-verified information.
- A deterministic safety-routing function identifies configured warning conditions.
- A state transition function records auditable transitions and prevents automatic downgrades from urgent/emergency states.
- Synthetic tests cover ordinary distress, unanswered safety questions, current warning signs, and escalation persistence.

## Run locally

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q
python -m src.demo
```

## Project layout

```text
src/
  __init__.py
  models.py
  safety.py
  demo.py
tests/
  test_safety.py
requirements.txt
```

## Safety limitations

The rules are conservative prototype routing rules, not a validated clinical risk score. A negative or missing model output must never be treated as proof of safety. Real deployment requires clinical review, privacy/security review, local emergency-resource configuration, a staffed human escalation process, and evaluation with qualified professionals. Do not use real patient data in this prototype.

## References for further review

- NICE NG222: https://www.nice.org.uk/guidance/NG222
- WHO mhGAP Intervention Guide: https://iris.who.int/bitstream/handle/10665/250239/9789241549790-eng.pdf

These are design references, not evidence that this prototype is clinically approved or compliant.
