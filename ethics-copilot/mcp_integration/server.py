from mcp.server import MCPServer

from mcp_integration.tools.ethics_cases import (
    create_ethics_case
)

from mcp_integration.tools.reports import (
    generate_ethics_report
)

from mcp_integration.tools.outlook import (
    send_outlook_email
)


mcp = MCPServer(
    "Ethics Copilot MCP Server"
)


@mcp.tool()
def create_case(
    employee_question: str,
    policy_section: str,
    policy_page: int,
    assessment: str
) -> dict:
    """Create a new ethics case."""

    return create_ethics_case(
        employee_question,
        policy_section,
        policy_page,
        assessment
    )


@mcp.tool()
def create_report(
    case_id: str
) -> dict:
    """Generate an ethics report."""

    return generate_ethics_report(
        case_id
    )


@mcp.tool()
def send_email(
    recipient: str,
    subject: str,
    body: str
) -> dict:
    """Send an ethics report through Outlook."""

    return send_outlook_email(
        recipient,
        subject,
        body
    )


if __name__ == "__main__":
    mcp.run()