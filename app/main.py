from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.agent import splunk_agent

app = FastAPI(
    title="Agentic Splunk SRE",
    description="API for the Google ADK Agent that queries Splunk.",
    version="1.0.0"
)

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse, summary="Chat with the Splunk Agent")
async def chat_endpoint(request: ChatRequest):
    try:
        response = splunk_agent.invoke(request.prompt)
        return ChatResponse(reply=response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

