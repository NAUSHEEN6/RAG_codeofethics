import asyncio

from mcp import Client

from mcp_integration.server import mcp


async def call_tool(
    tool_name: str,
    arguments: dict
):

    async with Client(mcp) as client:

        result = await client.call_tool(
            tool_name,
            arguments
        )

        return result


def run_tool(
    tool_name: str,
    arguments: dict
):

    return asyncio.run(
        call_tool(
            tool_name,
            arguments
        )
    )