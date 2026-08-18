
from rue.memory.conversation import Conversation
from rue.models.message import Message, Role
from pydantic import BaseModel

from rue.prompt.context import PromptContext



class SlidingWindowContextManager(BaseModel):
    
    max_tokens: int


    def build(
        self, conversation: Conversation
    ) -> PromptContext:
            
        messages = conversation.get_messages()

        system_messsages = [msg for msg in messages if msg.role == Role.SYSTEM]
        conversation_messages = [msg for msg in messages if msg.role != Role.SYSTEM]

        history = []
        token_count = 0

        for msg in reversed(conversation_messages):
            cost = self._count_tokens(msg.context)
            if token_count + cost > self.max_tokens:
                break
            history.insert(0, msg)
            token_count += cost
        return PromptContext(messages = system_messsages + history)

    

