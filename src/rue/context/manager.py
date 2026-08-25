
from rue.memory.conversation import Conversation
from rue.models.message import Message, Role
from pydantic import BaseModel

from rue.prompt.context import PromptContext



class SlidingWindowContextManager(BaseModel):
    
    max_tokens: int


    def build(
        self, conversation: Conversation
    ) -> list[Message]:
            
        messages = conversation.get_messages()

        system_messages = [msg for msg in messages if msg.role == Role.SYSTEM]
        conversation_messages = [msg for msg in messages if msg.role != Role.SYSTEM]

        history = []
        token_count = 0

        for msg in reversed(conversation_messages):
            cost = self._count_tokens(msg.content)
            if token_count + cost > self.max_tokens:
                break
            history.insert(0, msg)
            token_count += cost
        return system_messages + history
    
    def _count_tokens(self, text: str) -> int:
        chinses_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        others_chars = len(text) - chinses_chars
        return int(chinses_chars * 1.5 + others_chars * 0.75)

    

