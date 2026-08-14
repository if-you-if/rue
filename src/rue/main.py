from rue.llm.ollama import OllamaLLM
from rue.prompt import DEFAULT_PROMPT
from rue.models.message import ChatRequest,Message,Role
from rue.models.response import ChatResponse
from rue.memory.conversation import Conversation



def main():
   
    llm = OllamaLLM()

    conversation = Conversation()

    print("=" * 50)
    print("Ollama 交互式终端已启动！输入 'exit' 或 'quit' 结束对话。")
    print("=" * 50)

    while True:
        try:

            user_input = input("\nUser >").strip()

            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("再见！")
                break
            content = DEFAULT_PROMPT.format(question=user_input)
            message = Message(
                role=Role.USER,
                content=content
            )

            chat_request = ChatRequest(
                message=message
            )

            print("Assistant > ", end="", flush=True)

            chat_response = llm.chat(
                chat_request=chat_request, conversation=conversation)

            print(chat_response.content)
            
        except KeyboardInterrupt:
            print("\n检测到中断信号，程序已退出。")
            break
        except Exception as e:
            print(f"\n[错误]: 请求失败，原因: {e}")

if __name__ == "__main__":
    main()