from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

XAI_KEY = os.getenv("XAI_KEY")

@app.post("/v1/chat/completions")
async def proxy(request: Request):
    headers = {"Authorization": f"Bearer {XAI_KEY}"}
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.x.ai/v1/chat/completions",
            headers=headers,
            json=await request.json(),
            timeout=30.0
        )
    return resp.json()

@app.get("/")
async def root():
    return {"status": "ok", "message": "Grok proxy is running"}
