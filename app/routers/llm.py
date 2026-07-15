from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from app.services.llm_service import LLMService

router = APIRouter(prefix="/api/llm", tags=["LLM"])

class ChatMessage(BaseModel):
    role: str
    content: str

class LLMRequest(BaseModel):
    messages: List[ChatMessage]
    systemPrompt: str
    skillCategory: Optional[str] = None
    maxTokens: Optional[int] = None

@router.post("")
async def generate_chat(req: LLMRequest):
    try:
        formatted_messages = [{"role": m.role, "content": m.content} for m in req.messages]
        reply = await LLMService.call_llm(
            messages=formatted_messages,
            system_prompt=req.systemPrompt,
            skill_category=req.skillCategory,
            max_tokens=req.maxTokens
        )
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
