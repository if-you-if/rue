
from rue.models.message import Message


class Conversation:

    def __init__(self, system_message: Message):
        self.messages = [system_message]

    def add_user_message(self, user_message: Message):
        self.messages.append(user_message)

    def add_assistant_message(self, assistant_message: Message):
        self.messages.append(assistant_message)

    def get_messages(self):
        return list(self.messages)  
    
    def empty(self):
        return len(self.messages) == 0
