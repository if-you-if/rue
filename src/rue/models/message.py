class Message:
    def __init__(self, role: str, content: str, message_id: int):
        
        if role not in ["user", "assistant", "system"]:
            raise ValueError("Invalid role")

        self.role = role
        self.content = content
        self.message_id = message_id
    
    def to_dict(self):
        return {
            "role": self.role,
            "content": self.content,
            "message_id": self.message_id
        }

class ChatRequest:
    
    def __init__(self, message: Message, request_id: int):
        self.message = message
        self.request_id = request_id
    

