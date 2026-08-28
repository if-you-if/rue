from rue.config import PROJECT_ROOT
from rue.llm.ollama import OllamaLLM
from rue.prompt import DEFAULT_SYSTEM_PROMPT
from rue.models.message import Message,Role
from rue.memory.conversation import Conversation
from rue.context.manager import SlidingWindowContextManager
from rue.prompt.builder import PromptBuilder  
from rue.pipeline.chat import ChatPipeline
from rue.prompt.strategy import RAGStrategy
from rue.rag.embedding import get_embedding
from rue.rag.loader.text import TextLoader
from rue.rag.pipeline import RAGPipeline
from rue.rag.splitter.recursive import RecursiveCharacterSplitter
from rue.rag.retriever.vector import VectorRetriever
from rue.rag.store.chroma import ChromaVectorStore



def main():
   
    llm = OllamaLLM()

    context_manager = SlidingWindowContextManager(
        max_tokens = 2048
    )
    prompt_builder = PromptBuilder(strategy=RAGStrategy())
    
    conversation = Conversation(
        system_message=Message(
            role=Role.SYSTEM,
            content=DEFAULT_SYSTEM_PROMPT.format(domain="python"))
    )

    loader = TextLoader()
    splitter = RecursiveCharacterSplitter(chunk_size=500, chunk_overlap=50)
    embedding = get_embedding()
    store = ChromaVectorStore()
    retriever = VectorRetriever(embedding=embedding, store=store)
    

    rag_pipeline = RAGPipeline(
        loader=loader,
        splitter=splitter,
        embedding=embedding,
        store = store,
        retriever=retriever
    )
    rag_pipeline.index_directory(str(PROJECT_ROOT / "data" / "raw"))

    #组装 pipeline
    pipeline = ChatPipeline(
        llm=llm,
        context_manager=context_manager,
        prompt_builder=prompt_builder,
        conversation=conversation,
        rag_pipeline=rag_pipeline
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