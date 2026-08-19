from rue.llm.ollama import OllamaLLM
from rue.prompt import DEFAULT_SYSTEM_PROMPT
from rue.models.message import ChatRequest,Message,Role
from rue.models.response import ChatResponse
from rue.memory.conversation import Conversation
from rue.context.manager import SlidingWindowContextManager
from rue.prompt.builder import PromptBuilder  
from rue.pipeline.chat import ChatPipeline


def main():
   
    llm = OllamaLLM()

    context_manager = SlidingWindowContextManager(
        max_tokens = 2048
    )
    prompt_builder = PromptBuilder()
    
    conversation = Conversation(
        system_message=Message(
            role=Role.SYSTEM,
            content=DEFAULT_SYSTEM_PROMPT.format(domain="python"))
    )

    #组装 pipeline
    pipeline = ChatPipeline(
        llm=llm,
        context_manager=context_manager,
        prompt_builder=prompt_builder,
        conversation=conversation
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

            print("Assistant > ", end="", flush=True)


            for token in pipeline.run_stream(message):
                print(token, end="", flush=True)
            
        except KeyboardInterrupt:
            print("\n检测到中断信号，程序已退出。")
            break
        except Exception as e:
            print(f"\n[错误]: 请求失败，原因: {e}")

if __name__ == "__main__":
    main()