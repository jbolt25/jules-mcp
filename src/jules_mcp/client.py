from __future__ import annotations

import os
from typing import Any

import httpx


class JulesAPIError(RuntimeError):
    pass


class JulesClient:
    def __init__(self, api_key: str | None = None, base_url: str | None = None) -> None:
        self.api_key = api_key or os.getenv("JULES_API_KEY")
        if not self.api_key:
            raise RuntimeError("JULES_API_KEY is not set")
        self.base_url = (base_url or os.getenv("JULES_API_BASE") or "https://jules.googleapis.com/v1alpha").rstrip("/")

    async def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        headers = kwargs.pop("headers", {})
        headers["x-goog-api-key"] = self.api_key
        async with httpx.AsyncClient(base_url=self.base_url, timeout=30.0) as client:
            response = await client.request(method, path, headers=headers, **kwargs)
        if response.status_code >= 400:
            detail = response.text[:1000]
            raise JulesAPIError(f"Jules API {response.status_code}: {detail}")
        if response.status_code == 204 or not response.content:
            return {}
        return response.json()

    async def list_sources(self, page_size: int = 100, page_token: str | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {"pageSize": max(1, min(page_size, 100))}
        if page_token:
            params["pageToken"] = page_token
        return await self._request("GET", "/sources", params=params)

    async def list_sessions(self, page_size: int = 30, page_token: str | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {"pageSize": max(1, min(page_size, 100))}
        if page_token:
            params["pageToken"] = page_token
        return await self._request("GET", "/sessions", params=params)

    async def get_session(self, session_id: str) -> dict[str, Any]:
        return await self._request("GET", f"/sessions/{self._id(session_id, 'sessions')}")

    async def list_activities(self, session_id: str, page_size: int = 50, page_token: str | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {"pageSize": max(1, min(page_size, 100))}
        if page_token:
            params["pageToken"] = page_token
        sid = self._id(session_id, "sessions")
        return await self._request("GET", f"/sessions/{sid}/activities", params=params)

    async def send_message(self, session_id: str, prompt: str) -> dict[str, Any]:
        sid = self._id(session_id, "sessions")
        return await self._request("POST", f"/sessions/{sid}:sendMessage", json={"prompt": prompt})

    async def approve_plan(self, session_id: str) -> dict[str, Any]:
        sid = self._id(session_id, "sessions")
        return await self._request("POST", f"/sessions/{sid}:approvePlan", json={})

    async def create_session(
        self,
        *,
        prompt: str,
        source: str | None = None,
        branch: str | None = None,
        title: str | None = None,
        require_plan_approval: bool = True,
        auto_create_pr: bool = False,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "prompt": prompt,
            "requirePlanApproval": require_plan_approval,
        }
        if title:
            body["title"] = title
        if auto_create_pr:
            body["automationMode"] = "AUTO_CREATE_PR"
        if source:
            source_name = source if source.startswith("sources/") else f"sources/{source}"
            ctx: dict[str, Any] = {"source": source_name}
            if branch:
                ctx["githubRepoContext"] = {"startingBranch": branch}
            body["sourceContext"] = ctx
        return await self._request("POST", "/sessions", json=body)

    @staticmethod
    def _id(value: str, prefix: str) -> str:
        return value[len(prefix) + 1 :] if value.startswith(prefix + "/") else value
