from .base import BaseLLM
from rue.models.message import ChatRequest
from rue.models.response import ChatResponse
import httpx
from rue.config import settings
from rue.memory.conversation import Conversation
from rue.models.message import Message, Role

class OllamaLLM(BaseLLM):

    def chat(self, messages: list[Message]) -> ChatResponse:

        endpoint = f"{settings.base_url.rstrip('/')}/api/chat"
        
        payload = {
            "model": settings.model_name,
            "stream": False,
            "messages": [{"role": msg.role.value, "content": msg.content} for msg in messages]
        }

        with httpx.Client() as client:
            res = client.post(endpoint, json=payload, timeout=60.0)
            res.raise_for_status()
            data = res.json()
       
            ressponse = ChatResponse(
            content=data['message']['content'],
            model=data.get("model", settings.model_name)
            )
            return ressponse
    
    def chat_stream(self, messages: list[Message]) -> Iterator[str]:
        return super().chat_stream(messages)
        