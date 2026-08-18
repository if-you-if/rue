from abc import ABC, abstractmethod
from rue.models.response import ChatResponse
from rue.models.message import Message


class BaseLLM(ABC):
    
    @abstractmethod
    def chat(self, messages: list[Message]) -> ChatResponse:
        pass