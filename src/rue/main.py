from rue.llm.ollama import OllamaLLM
from rue.prompt import DEFAULT_SYSTEM_PROMPT
from rue.models.message import ChatRequest,Message,Role
from rue.models.response import ChatResponse
from rue.memory.conversation import Conversation
from rue.context.manager import SlidingWindowContextManager


def main():
   
    llm = OllamaLLM()

    context_manager = SlidingWindowContextManager(
        max_turns = 5
    )
    
    conversation = Conversation(system_message=Message(
        role=Role.SYSTEM,
        content=DEFAULT_SYSTEM_PROMPT.format(domain="python"))
    )

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

            message = Message(
                role=Role.USER,
                content=user_input
            )

            conversation.add_user_message(message)
            messages = context_manager.build(conversation=conversation)
            

            print("Assistant > ", end="", flush=True)

            chat_response = llm.chat(
                messages=messages)
            
            assistant_message = Message(role=Role.ASSISTANT, content=chat_response.content)
            
            conversation.add_assistant_message(assistant_message)

            print(chat_response.content)
            
        except KeyboardInterrupt:
            print("\n检测到中断信号，程序已退出。")
            break
        except Exception as e:
            print(f"\n[错误]: 请求失败，原因: {e}")

if __name__ == "__main__":
    main()