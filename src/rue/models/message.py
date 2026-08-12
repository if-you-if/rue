from pydantic import BaseModel, Field
from enum import Enum
import uuid

class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class Message(BaseModel):
    
    role: Role
    content: str
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    

class ChatRequest(BaseModel):
    message: Message
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    

