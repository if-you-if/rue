from .template import PromptTemplate

DEFAULT_PROMPT = PromptTemplate(

    """
你是一个智能助手。

请回答用户的问题：

{question}

"""

)