import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from mcp_integration.client import run_tool


def main():

    print("=" * 60)
    print("MCP CLIENT TEST")
    print("=" * 60)

    result = run_tool(
        "create_case",
        {
            "employee_question":
                "What is SpeakUp?",

            "policy_section":
                "1.3 SpeakUp",

            "policy_page":
                11,

            "assessment":
                "SpeakUp is a web and phone-based ethics concerns "
                "reporting and incident management tool."
        }
    )

    print("\nMCP RESULT:")
    print(result)

    print("\n" + "=" * 60)
    print("MCP TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()