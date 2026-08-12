from abc import ABC, abstractmethod
from rue.models.message import ChatRequest
from rue.models.response import ChatResponse


class BaseLLM(ABC):
    
    @abstractmethod
    def chat(self, chat_request: ChatRequest) -> ChatResponse:
        pass