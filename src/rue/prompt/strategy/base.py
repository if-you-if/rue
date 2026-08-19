from abc import ABC, abstractmethod
from rue.prompt.context import PromptContext
from rue.models.message import Message

class PromptStrategy(ABC):

    @abstractmethod
    def build(self, context: PromptContext) -> list[Message]:
        return list(context.messages)
    