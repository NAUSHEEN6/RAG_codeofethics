import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from mcp_integration.client import run_tool


def main():

    print("=" * 60)
    print("MCP REPORT TEST")
    print("=" * 60)

    result = run_tool(
        "create_report",
        {
            "case_id": "ETH-0001"
        }
    )

    print("\nREPORT RESULT:")
    print(result)

    print("\n" + "=" * 60)
    print("REPORT TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()