"""FastAPI front‑end – exposes a single `/ask` endpoint."""

import asyncio

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .agent import ask

app = FastAPI(title="WildFly AI Assist", version="0.1.0")


class Query(BaseModel):
    """Request payload schema."""

    log: str = Field(..., description="Raw WildFly stack trace or free‑form question")


@app.post("/ask")
async def ask_endpoint(payload: Query):
    """Run the heavy work in a thread — keeps the event‑loop non‑blocking."""
    if not payload.log.strip():
        raise HTTPException(status_code=400, detail="Empty log")

    answer = await asyncio.to_thread(ask, payload.log)
    return {"answer": answer}
