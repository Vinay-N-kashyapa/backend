import httpx
import logging
from typing import List, Dict, Optional
from app.config import settings

logger = logging.getLogger("pinit.llm")

class LLMService:
    @staticmethod
    async def call_llm(
        messages: List[Dict[str, str]],
        system_prompt: str,
        skill_category: Optional[str] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        is_soft_skill = skill_category in ['soft-skills', 'communication', 'leadership']
        primary_provider = 'groq' if is_soft_skill else 'openrouter'

        if primary_provider == 'openrouter':
            try:
                return await LLMService._execute_openrouter(messages, system_prompt, max_tokens)
            except Exception as e:
                logger.warning(f"OpenRouter primary call failed, trying Groq fallback: {e}")
                return await LLMService._execute_groq(messages, system_prompt, max_tokens)
        else:
            try:
                return await LLMService._execute_groq(messages, system_prompt, max_tokens)
            except Exception as e:
                logger.warning(f"Groq primary call failed, trying OpenRouter fallback: {e}")
                return await LLMService._execute_openrouter(messages, system_prompt, max_tokens)

    @staticmethod
    async def _execute_groq(messages: List[Dict[str, str]], system_prompt: str, max_tokens: Optional[int]) -> str:
        # Support multiple comma-separated keys
        keys = [k.strip() for k in settings.groq_api_key.split(",") if k.strip()]
        if not keys:
            raise ValueError("No Groq keys configured")

        async with httpx.AsyncClient() as client:
            last_err = None
            for key in keys:
                try:
                    payload = {
                        "model": "llama-3.3-70b-versatile",
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            *messages
                        ],
                        "max_tokens": max_tokens or 300,
                        "temperature": 0.7
                    }
                    res = await client.post(
                        "https://api.groq.com/openai/v1/chat/completions",
                        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                        json=payload,
                        timeout=12.0
                    )
                    if res.status_code == 200:
                        data = res.json()
                        return data["choices"][0]["message"]["content"].strip()
                    else:
                        raise Exception(f"Groq API returned {res.status_code}: {res.text}")
                except Exception as err:
                    last_err = err
            raise last_err

    @staticmethod
    async def _execute_openrouter(messages: List[Dict[str, str]], system_prompt: str, max_tokens: Optional[int]) -> str:
        if not settings.openrouter_api_key:
            raise ValueError("No OpenRouter key configured")

        async with httpx.AsyncClient() as client:
            payload = {
                "model": "qwen/qwen-2.5-coder-32b-instruct",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    *messages
                ],
                "max_tokens": max_tokens or 1000,
                "temperature": 0.2
            }
            res = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.openrouter_api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://pinit-de424.web.app",
                    "X-Title": "Pi Career OS"
                },
                json=payload,
                timeout=15.0
            )
            if res.status_code == 200:
                data = res.json()
                return data["choices"][0]["message"]["content"].strip()
            else:
                raise Exception(f"OpenRouter API returned {res.status_code}: {res.text}")
