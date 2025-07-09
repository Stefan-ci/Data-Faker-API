from utils.base import BaseDataGenerator, Constants


class ChatGenerator(BaseDataGenerator):
    def generate(self, n=Constants.DATA_GENERATION_LENGTH.value): # type: ignore
        return [
            {
                "id": i,
                "uuid": self.fake.uuid4(),
                "sender": self.fake.name(),
                "receiver": self.fake.name(),
                "message": self.fake.sentence(),
                "timestamp": self.fake.date_time(),
                "is_read": self.fake.boolean()
            }
            for i in range(1, n + 1)
        ]


def generate_chats_data(length=Constants.DATA_GENERATION_LENGTH.value):
    return ChatGenerator().generate(n=length)
