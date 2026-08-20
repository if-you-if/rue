
from rue.prompt.context import PromptContext
from rue.prompt.strategy.base import PromptStrategy
from rue.models.message import Message, Role


class RAGStrategy(PromptStrategy):

    def build(self, context: PromptContext) -> list[Message]:
        messages = list(context.messages)

        # 插在system消息之后，对话历史之前
        if context.retrieved_context:
            rag_message = Message(
                role=Role.SYSTEM,
                content="请根据以下参考资料回答问题。如果资料不足以回答, 请如实说明。\n\n"
                        f"参考资料: \n{context.retrieved_context}"
            )
            # 找到最后一个system消息的位置，插在其后面
            insert_idx = 1
            for i, msg in enumerate(messages):
                if msg.role == Role.SYSTEM:
                    insert_idx = i + 1
            messages.insert(insert_idx, rag_message)
        return messages