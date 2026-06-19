from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

XAI_KEY = os.getenv("XAI_KEY")
PROXY_TOKEN = "grokproxy"

@app.post("/v1/chat/completions")
async def proxy(request: Request):
    auth = request.headers.get("authorization")
    if not auth or not auth.startswith("Bearer ") or auth.split(" ")[1] != PROXY_TOKEN:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Invalid token")

    body = await request.json()
    body["model"] = "grok-4"   # Force valid model

    headers = {"Authorization": f"Bearer {XAI_KEY}"}
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.x.ai/v1/chat/completions",
            headers=headers,
            json=body,
            timeout=30.0
        )
    return resp.json()
