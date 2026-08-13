from .base import BaseLLM
from rue.models.message import ChatRequest
from rue.models.response import ChatResponse
import httpx
from rue.config import settings

class OllamaLLM(BaseLLM):

    def chat(self, chat_request: ChatRequest) -> ChatResponse:
       
        endpoint = f"{settings.base_url.rstrip('/')}/api/chat"
        
        payload = {
            "model": settings.model_name,
            "stream": False,
            "messages": [chat_request.message.model_dump(mode="json")]
        }

        with httpx.Client() as client:
            res = client.post(endpoint, json=payload, timeout=60.0)
            res.raise_for_status()
            data = res.json()
       
        return ChatResponse(
            content=data['message']['content'],
            model=data.get("model", settings.model_name)
        )