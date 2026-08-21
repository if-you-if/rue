import logging

logger = logging.getLogger(__name__)

from rue.memory.conversation import Conversation
from rue.context.manager import SlidingWindowContextManager
from rue.llm.base import BaseLLM
from rue.prompt.builder import PromptBuilder
from rue.models.message import Message, Role
from rue.models.response import ChatResponse
from typing import Iterator

from rue.rag.pipeline import RAGPipeline


class ChatPipeline:

    def __init__(
        self, 
        llm: BaseLLM,
        context_manager: SlidingWindowContextManager, 
        prompt_builder: PromptBuilder, 
        conversation: Conversation,
        rag_pipeline: RAGPipeline | None = None
    ):
        self.llm = llm
        self.context_manager = context_manager
        self.prompt_builder = prompt_builder
        self.conversation = conversation
        self.rag_pipeline = rag_pipeline
    
    def _retrieve_context(self, query: str) -> str:
        """RAG 检索，失败时降级为空上下文"""
        if not self.rag_pipeline:
            return ""
        try:
            return self.rag_pipeline.retrieve_as_context(query)
        except Exception as e:
            logger.warning(f"RAG 检索失败, 降级为纯对话模式: {e}")
            return ""    

    def run(self, user_message: Message) -> ChatResponse:

        # 1.存入对话历史
        self.conversation.add_user_message(user_message)

        # 2.构建上下文
        context =self.context_manager.build(conversation=self.conversation)

        context.retrieved_context = self._retrieve_context(user_message.content)

        # 3.组装prompt
        messages = self.prompt_builder.build(prompt_context=context)

        # 4.调用LLM
        response = self.llm.chat(messages=messages)

        # 5.存入助手回复
        self.conversation.add_assistant_message(Message(role=Role.ASSISTANT, content=response.content))

        return response

        

    def run_stream(
        self,
        user_message: Message
    ) -> Iterator[str]:
        self.conversation.add_user_message(user_message)
        context = self.context_manager.build(conversation=self.conversation)
        
        #RAG检索
        context.retrieved_context = self._retrieve_context(user_message.content)

        messages = self.prompt_builder.build(prompt_context=context)
        
        # 流式调用llm,逐token返回
        full_response = []
        for token in self.llm.chat_stream(messages=messages):
            full_response.append(token)
            yield token
        assistant_message = Message(
            role=Role.ASSISTANT,
            content="".join(full_response)
            )

        self.conversation.add_assistant_message(assistant_message=assistant_message)

    



