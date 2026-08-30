import json
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

CASE_FILE = PROJECT_ROOT / "ethics_cases.json"


def _load_cases():

    if not CASE_FILE.exists():
        return []

    with open(
        CASE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def _save_cases(cases):

    with open(
        CASE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            cases,
            file,
            indent=2
        )


def create_ethics_case(
    employee_question: str,
    policy_section: str,
    policy_page: int,
    assessment: str
):

    cases = _load_cases()

    case_id = (
        f"ETH-{len(cases) + 1:04d}"
    )

    case = {

        "case_id": case_id,

        "created_at":
            datetime.now().isoformat(),

        "employee_question":
            employee_question,

        "policy_section":
            policy_section,

        "policy_page":
            policy_page,

        "assessment":
            assessment,

        "status":
            "OPEN"
    }

    cases.append(case)

    _save_cases(cases)

    return case