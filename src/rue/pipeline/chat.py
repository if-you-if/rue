from pydantic import BaseModel
from rue.memory.conversation import Conversation
from rue.context.manager import SlidingWindowContextManager
from rue.llm.ollama import OllamaLLM
from rue.prompt.builder import PromptBuilder

class ChatPipeline(BaseModel):
    
    llm: OllamaLLM
    context_manager: SlidingWindowContextManager
    prompt_builder: PromptBuilder
    conversation: Conversation

    def run(self, user_message: Message) -> ChatResponse:

        # 1.存入对话历史
        self.conversation.add_user_message(user_message)

        # 2.构建上下文
        context =self.context_manager.build(self.conversation)

        # 3.组装prompt
        messages = self.prompt_builder.build(context, self.conversation)

        # 4.调用LLM
        response = self.llm.chat(messages)

        # 5.存入助手回复
        self.conversation.add_assistant_message(response)

        return response

        

        



