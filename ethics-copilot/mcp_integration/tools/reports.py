from pathlib import Path
import json


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
    .parent
)

CASE_FILE = (
    PROJECT_ROOT /
    "ethics_cases.json"
)


def generate_ethics_report(
    case_id: str
):

    if not CASE_FILE.exists():

        raise ValueError(
            "No ethics cases exist."
        )

    with open(
        CASE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        cases = json.load(file)

    case = next(
        (
            case
            for case in cases
            if case["case_id"] == case_id
        ),
        None
    )

    if case is None:

        raise ValueError(
            f"Case {case_id} not found."
        )

    report = f"""
ETHICS CASE REPORT
==================

Case ID:
{case["case_id"]}

Created:
{case["created_at"]}

Employee Question:
{case["employee_question"]}

Policy Section:
{case["policy_section"]}

Policy Page:
{case["policy_page"]}

Assessment:
{case["assessment"]}

Status:
{case["status"]}
"""

    report_file = (
        PROJECT_ROOT /
        f"{case_id}_report.txt"
    )

    report_file.write_text(
        report.strip(),
        encoding="utf-8"
    )

    return {
        "case_id": case_id,
        "report": report,
        "file": str(report_file)
    }