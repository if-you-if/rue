class ChatResponse:
    def __init__(self, content: str, model: str):
        self.content = content
        self.model = model

    def to_dict(self):
        return {
            "content": self.content,
            "model": self.model
        }


