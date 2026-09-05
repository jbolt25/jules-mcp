from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from .client import JulesClient

mcp = FastMCP("jules-mcp")


def _client() -> JulesClient:
    return JulesClient()


@mcp.tool()
async def jules_list_sources(page_size: int = 100) -> dict[str, Any]:
    """List repositories connected to the authenticated Jules account."""
    return await _client().list_sources(page_size=page_size)


@mcp.tool()
async def jules_list_sessions(page_size: int = 30) -> dict[str, Any]:
    """List recent Jules sessions."""
    return await _client().list_sessions(page_size=page_size)


@mcp.tool()
async def jules_start(
    prompt: str,
    source: str | None = None,
    branch: str | None = None,
    title: str | None = None,
    require_plan_approval: bool = True,
    auto_create_pr: bool = False,
) -> dict[str, Any]:
    """Start a Jules coding session. Plan approval defaults to required."""
    return await _client().create_session(
        prompt=prompt,
        source=source,
        branch=branch,
        title=title,
        require_plan_approval=require_plan_approval,
        auto_create_pr=auto_create_pr,
    )


@mcp.tool()
async def jules_status(session_id: str) -> dict[str, Any]:
    """Get the current state and metadata for a Jules session."""
    return await _client().get_session(session_id)


@mcp.tool()
async def jules_activity(session_id: str, page_size: int = 50) -> dict[str, Any]:
    """Read Jules session activities, including plans, messages, and progress."""
    return await _client().list_activities(session_id, page_size=page_size)


@mcp.tool()
async def jules_send(session_id: str, message: str) -> dict[str, Any]:
    """Send feedback, an answer, or additional instructions to an active Jules session."""
    return await _client().send_message(session_id, message)


@mcp.tool()
async def jules_approve_plan(session_id: str) -> dict[str, Any]:
    """Explicitly approve a pending Jules plan."""
    return await _client().approve_plan(session_id)


@mcp.tool()
async def jules_result(session_id: str) -> dict[str, Any]:
    """Retrieve the full session object, including outputs when completed."""
    return await _client().get_session(session_id)


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
