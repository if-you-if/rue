from rue.prompt.context import PromptContext
from rue.prompt.strategy.base import PromptStrategy
from rue.models.message import Message
from rue.prompt.strategy.chat import ChatStrategy


class PromptBuilder:

    def __init__(self, strategy: PromptStrategy | None = None):
        self.strategy = strategy or ChatStrategy()

    def build(self, prompt_context: PromptContext) -> list[Message]:
        return self.strategy.build(prompt_context)

        


