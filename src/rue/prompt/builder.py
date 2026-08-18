from rue.models.message import Message
from rue.prompt.context import PromptContext
from rue.models.message import Role

class PromptBuilder:

    def build(
        self,
        prompt_context: PromptContext,
    ) -> list[Message]:
        
        messages = list(prompt_context.messages)

        if prompt_context.retrieved_context:

            messages.insert(
                0,
                Message(
                    role=Role.SYSTEM,
                    content="参考资料:\n"
                        + prompt_context.retrieved_context,
                )
            )

        return messages
        


