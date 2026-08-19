from rue.prompt.context import PromptContext
from rue.models.message import Message
from rue.prompt.strategy.base import PromptStrategy

class ChatStrategy(PromptStrategy):

    def build(self, context: PromptContext) -> list[Message]:
        return list(context.messages)