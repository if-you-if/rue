from .template import PromptTemplate

DEFAULT_SYSTEM_PROMPT = PromptTemplate(

    """
你是一个智能助手。

非常擅长：

{domain}

的问题

"""

)