import pytest
import respx
from httpx import Response

from jules_mcp.client import JulesClient


@pytest.mark.asyncio
@respx.mock
async def test_create_session_requires_plan_approval_by_default() -> None:
    route = respx.post("https://jules.googleapis.com/v1alpha/sessions").mock(
        return_value=Response(200, json={"name": "sessions/123", "state": "QUEUED"})
    )

    client = JulesClient(api_key="test-key")
    result = await client.create_session(
        prompt="Fix the bug",
        source="sources/github-owner-repo",
        branch="main",
    )

    assert result["state"] == "QUEUED"
    request = route.calls.last.request
    assert request.headers["x-goog-api-key"] == "test-key"
    assert b'"requirePlanApproval":true' in request.content


@pytest.mark.asyncio
@respx.mock
async def test_send_message_accepts_resource_name() -> None:
    route = respx.post(
        "https://jules.googleapis.com/v1alpha/sessions/abc:sendMessage"
    ).mock(return_value=Response(200, json={}))

    client = JulesClient(api_key="test-key")
    await client.send_message("sessions/abc", "Proceed with option two")

    assert route.called
