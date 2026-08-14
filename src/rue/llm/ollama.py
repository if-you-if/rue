from .base import BaseLLM
from rue.models.message import ChatRequest
from rue.models.response import ChatResponse
import httpx
from rue.config import settings
from rue.memory.conversation import Conversation
from rue.models.message import Message, Role

class OllamaLLM(BaseLLM):

    def chat(self, chat_request: ChatRequest, conversation: Conversation = None) -> ChatResponse:

        if conversation is None:
            conversation = Conversation()
        conversation.add_user_message(chat_request.message)
       
        endpoint = f"{settings.base_url.rstrip('/')}/api/chat"
        
        payload = {
            "model": settings.model_name,
            "stream": False,
            "messages": [msg.model_dump(mode="json") for msg in conversation.messages]
        }

        with httpx.Client() as client:
            res = client.post(endpoint, json=payload, timeout=60.0)
            res.raise_for_status()
            data = res.json()
       
            ressponse = ChatResponse(
            content=data['message']['content'],
            model=data.get("model", settings.model_name)
            )
            assistant_message = Message(
                role=Role.ASSISTANT,
                content=ressponse.content
            )
            conversation.add_assistant_message(assistant_message)
            return ressponse