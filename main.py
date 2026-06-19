from fastapi import FastAPI, Request, HTTPException
import httpx
import os

app = FastAPI()

XAI_KEY = os.getenv("XAI_KEY")
PROXY_TOKEN = "grokproxy"

SYSTEM_PROMPT = "You are Ara, a friendly, warm, and helpful female AI assistant. You have a pleasant personality and speak naturally."

@app.post("/v1/chat/completions")
async def proxy(request: Request):
    auth = request.headers.get("authorization")
    if not auth or not auth.startswith("Bearer ") or auth.split(" ")[1] != PROXY_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")

    body = await request.json()
    body["model"] = "grok-4"

    # Add system prompt if not already present
    if not any(msg.get("role") == "system" for msg in body.get("messages", [])):
        body.setdefault("messages", []).insert(0, {"role": "system", "content": SYSTEM_PROMPT})

    headers = {"Authorization": f"Bearer {XAI_KEY}"}
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.x.ai/v1/chat/completions",
            headers=headers,
            json=body,
            timeout=30.0
        )
    return resp.json()
