from rue.llm.ollama import OllamaLLM
from rue.prompt import DEFAULT_PROMPT
from rue.models.message import ChatRequest,Message,Role
from rue.models.response import ChatResponse


def main():
   
    llm = OllamaLLM()
    
    content = DEFAULT_PROMPT.format(
        question="介绍一下自己")

    message = Message(
        role=Role.USER,
        content=content
    )

    chat_request = ChatRequest(
        message=message
    )

    chat_response = llm.chat(
        chat_request=chat_request)

    print(chat_response.model_dump(mode="json"))

if __name__ == "__main__":
    main()