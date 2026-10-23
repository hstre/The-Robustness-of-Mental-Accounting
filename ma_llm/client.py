"""Minimal async OpenRouter chat-completions client with retries."""

from __future__ import annotations

import asyncio
import os
import random
from typing import Any

import httpx

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODELS_URL = "https://openrouter.ai/api/v1/models"


class OpenRouterError(RuntimeError):
    pass


class OpenRouterClient:
    def __init__(self, api_key: str | None = None, timeout: float = 180.0, max_retries: int = 6):
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY")
        if not self.api_key:
            raise OpenRouterError("OPENROUTER_API_KEY is not set")
        self.max_retries = max_retries
        self._http = httpx.AsyncClient(
            timeout=timeout,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "X-Title": "Mental Accounting LLM replication",
            },
        )

    async def close(self) -> None:
        await self._http.aclose()

    async def chat(self, model: str, messages: list[dict], **params: Any) -> dict:
        """Return {"content", "reasoning", "usage", "provider", "finish_reason"}."""
        body = {"model": model, "messages": messages, "usage": {"include": True}}
        body.update({k: v for k, v in params.items() if v is not None})
        delay = 2.0
        for attempt in range(self.max_retries + 1):
            try:
                r = await self._http.post(API_URL, json=body)
            except (httpx.TransportError, httpx.TimeoutException) as e:
                err = f"transport: {e!r}"
            else:
                if r.status_code == 200:
                    try:
                        data = r.json()
                    except ValueError:
                        data = {"error": f"invalid JSON body: {r.text[:200]!r}"}
                    if "error" in data:
                        err = f"api error: {data['error']}"
                    elif not data.get("choices"):
                        err = "empty choices"
                    else:
                        ch = data["choices"][0]
                        msg = ch.get("message") or {}
                        return {
                            "content": msg.get("content") or "",
                            "reasoning": msg.get("reasoning"),
                            "usage": data.get("usage", {}),
                            "provider": data.get("provider"),
                            "finish_reason": ch.get("finish_reason"),
                        }
                elif r.status_code in (400, 401, 402, 403, 404):
                    raise OpenRouterError(f"{r.status_code}: {r.text[:500]}")
                else:
                    err = f"{r.status_code}: {r.text[:300]}"
            if attempt == self.max_retries:
                raise OpenRouterError(f"giving up after {attempt + 1} attempts: {err}")
            await asyncio.sleep(delay + random.uniform(0, 1))
            delay = min(delay * 2, 60)
        raise AssertionError("unreachable")


async def list_models() -> list[dict]:
    async with httpx.AsyncClient(timeout=60) as http:
        r = await http.get(MODELS_URL)
        r.raise_for_status()
        return r.json()["data"]
