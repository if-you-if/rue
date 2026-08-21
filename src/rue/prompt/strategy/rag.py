
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
                content="你是一个基于知识库的助手。请根据以下参考资料回答用户的问题。\n"
                        "要求：\n"
                        "1. 优先使用参考资料中的内容来回答，而不是你自己的知识。\n"
                        "2. 在回答中使用 [1]、[2] 等标注你引用了哪条参考资料。\n"
                        "3. 如果参考资料足以回答问题，请在回答末尾列出引用的来源文件。\n"
                        "4. 如果参考资料不足以回答，请如实说明。\n\n"
                        f"参考资料:\n{context.retrieved_context}"
            )
            # 找到最后一个system消息的位置，插在其后面
            insert_idx = 1
            for i, msg in enumerate(messages):
                if msg.role == Role.SYSTEM:
                    insert_idx = i + 1
            messages.insert(insert_idx, rag_message)
        return messages