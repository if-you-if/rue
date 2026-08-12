from .base import BaseLLM
from rue.models.message import ChatRequest
from rue.models.response import ChatResponse

class OllamaLLM(BaseLLM):

    def chat(self, chat_request: ChatRequest) -> ChatResponse:
        return ChatResponse(
            content=f"Ollama received: {chat_request.message.content}",
            model="qwen2.5:1.5b"
        )