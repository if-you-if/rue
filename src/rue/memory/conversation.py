
from rue.models.message import Message


class Conversation:

    def __init__(self):
        self.messages = []

    def add_user_message(self, user_message: Message):
        self.messages.append(user_message)

    def add_assistant_message(self, assistant_message: Message):
        self.messages.append(assistant_message)

    def get_messages(self):
        return list(self.messages)    
