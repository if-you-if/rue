from abc import ABC, abstractmethod
from rue.models.response import ChatResponse
from rue.models.message import Message
from typing import Iterator

class BaseLLM(ABC):
    
    @abstractmethod
    def chat(self, messages: list[Message]) -> ChatResponse:
        pass

    @abstractmethod
    def chat_stream(self, messages: list[Message])->Iterator[str]:
        pass