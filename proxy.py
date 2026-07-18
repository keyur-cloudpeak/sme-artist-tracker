"""
proxy.py — Lightweight FastAPI proxy for Anthropic API.

Runs in a background thread inside the Streamlit process on port 8502.
The browser JS posts to http://localhost:8502/chat (streaming NDJSON),
so the Anthropic API key NEVER leaves the Python server.
"""

from __future__ import annotations

import os
import json
import threading
import logging

import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import uvicorn

logger = logging.getLogger(__name__)

# ── Build app ──────────────────────────────────────────────────────────────

app = FastAPI(title="SME Pulse Proxy", docs_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    # Allow the Streamlit iframe origin (same host, different port/iframe).
    # In production narrow this to your actual domain.
    allow_origins=["*"],
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"


def _get_api_key() -> str:
    """Read the key from the environment at request time (not at import time)."""
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        # Also try Streamlit secrets when running inside Streamlit
        try:
            import streamlit as st
            key = st.secrets.get("ANTHROPIC_API_KEY", "")
        except Exception:
            pass
    return key


@app.post("/chat")
async def chat(request: Request):
    """
    Accepts the same JSON body that would go to Anthropic, strips any
    client-supplied auth headers, injects the server-side key, and
    streams the SSE response back to the browser.
    """
    api_key = _get_api_key()
    if not api_key:
        return StreamingResponse(
            iter([b'data: {"type":"error","error":"API key not configured on server."}\n\n']),
            media_type="text/event-stream",
            status_code=500,
        )

    try:
        body = await request.json()
    except Exception:
        return StreamingResponse(
            iter([b'data: {"type":"error","error":"Invalid JSON body."}\n\n']),
            media_type="text/event-stream",
            status_code=400,
        )

    # Force streaming on
    body["stream"] = True

    headers = {
        "x-api-key": api_key,
        "anthropic-version": ANTHROPIC_VERSION,
        "content-type": "application/json",
    }

    async def generate():
        async with httpx.AsyncClient(timeout=120) as client:
            async with client.stream(
                "POST", ANTHROPIC_URL, headers=headers, json=body
            ) as upstream:
                if upstream.status_code != 200:
                    err_text = await upstream.aread()
                    yield f"data: {json.dumps({'type': 'error', 'error': err_text.decode()[:200]})}\n\n".encode()
                    return
                async for chunk in upstream.aiter_bytes():
                    yield chunk

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.get("/health")
async def health():
    return {"status": "ok", "key_configured": bool(_get_api_key())}


# ── Singleton launcher ─────────────────────────────────────────────────────

_started = False
_lock = threading.Lock()

PROXY_PORT = 8502


def start_proxy_if_needed(port: int = PROXY_PORT) -> None:
    """
    Starts the uvicorn server in a daemon thread.
    Safe to call multiple times — starts only once per process.
    """
    global _started
    with _lock:
        if _started:
            return
        _started = True

    def _run():
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=port,
            log_level="warning",
            access_log=False,
        )

    t = threading.Thread(target=_run, daemon=True, name="anthropic-proxy")
    t.start()
    logger.info("Anthropic proxy started on port %d", port)
