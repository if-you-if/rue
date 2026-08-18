from pydantic import BaseModel
from rue.models.message import Message

class PromptContext(BaseModel):
    messages: list[Message]
    retrieved_context: str | None = None
    