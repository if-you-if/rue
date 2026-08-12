import uuid
from rue.llm.ollama import OllamaLLM
from rue.prompt import DEFAULT_PROMPT
from rue.models.message import ChatRequest,Message
from rue.models.response import ChatResponse


def main():
   
    llm = OllamaLLM()
    
    content = DEFAULT_PROMPT.format(
        question="介绍一下自己")

    message = Message(
        role="user",
        content=content,
        message_id = uuid.uuid4()
    )

    chat_request = ChatRequest(
        message=message,
        request_id=uuid.uuid4()
    )

    chat_response = llm.chat(
        chat_request=chat_request)

    print(chat_response.to_dict())

if __name__ == "__main__":
    main()