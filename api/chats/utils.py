from utils.base import BaseDataGenerator


class ChatGenerator(BaseDataGenerator):
    def generate(self, n=10): # type: ignore
        return [
            {
                "id": i,
                "uuid": self.fake.uuid4(),
                "sender": self.fake.name(),
                "receiver": self.fake.name(),
                "message": self.fake.sentence(),
                "timestamp": self.fake.date_time(),
                "read": self.fake.boolean()
            }
            for i in range(1, n + 1)
        ]


def generate_chats_data(length=10):
    return ChatGenerator().generate(n=length)
