from rue.rag.embedding.base import BaseEmbedding
from .base import BaseLLM
from rue.models.response import ChatResponse
import httpx
from rue.config import settings
from rue.models.message import Message, Role
from typing import Iterator
import json

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
        endpoint = f"{settings.base_url.rstrip('/')}/api/chat"
        payload = {
            "model": settings.model_name,
            "stream": True,
            "messages": [{"role": msg.role.value, "content": msg.content} for msg in messages]
        }

        with httpx.stream("POST", endpoint, json=payload, timeout=60.0) as res:
            res.raise_for_status()
            for line in res.iter_lines():
                if not line:
                    continue
                chunk = json.loads(line)
                if chunk.get("done"):
                    break
                yield chunk["message"]["content"]



