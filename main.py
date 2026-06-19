from fastapi import FastAPI
import httpx
import os

app = FastAPI()

XAI_KEY = os.getenv("XAI_KEY")

@app.post("/v1/chat/completions")
async def proxy(request):
    body = await request.json()
    if "model" in body:
        body = "grok-beta"
    
    headers = {"Authorization": f"Bearer {XAI_KEY}"}
    async with httpx.AsyncClient() as client:
        r = await client.post("https://api.x.ai/v1/chat/completions", headers=headers, json=body)
    return r.json()
