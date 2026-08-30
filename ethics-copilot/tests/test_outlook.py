import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from mcp_integration.client import run_tool


def main():

    recipient = input(
        "Enter YOUR Outlook email address: "
    ).strip()

    if not recipient:
        print("No recipient provided.")
        return

    print("\nSending test email through MCP...")

    result = run_tool(
        "send_email",
        {
            "recipient": recipient,
            "subject": "Ethics Copilot - MCP Test",
            "body": (
                "This is a test email sent through "
                "the Ethics Copilot MCP Outlook integration."
            )
        }
    )

    print("\nOUTLOOK RESULT:")
    print(result)


if __name__ == "__main__":
    main()