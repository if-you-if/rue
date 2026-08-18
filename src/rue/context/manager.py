
from rue.memory.conversation import Conversation
from rue.models.message import Message, Role
from pydantic import BaseModel



class SlidingWindowContextManager(BaseModel):
    
    max_turns: int


    def build(
        self, conversation: Conversation
    ) -> list[Message]:

        if conversation.empty():
            return []
        
        messages = conversation.get_messages()

        system_messages = [msg for msg in messages if msg.role == Role.SYSTEM]

        conversation_messages = [msg for msg in messages if msg.role != Role.SYSTEM]

        max_messages = self.max_turns * 2

        if max_messages <= 0:
            return system_messages

        return (
            system_messages 
            + 
            conversation_messages[-max_messages:]
        )

    

