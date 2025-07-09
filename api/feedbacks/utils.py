from utils.base import BaseDataGenerator, Constants


class FeedbackGenerator(BaseDataGenerator):
    def generate(self, n=Constants.DATA_GENERATION_LENGTH.value): # type: ignore
        return [
            {
                "id": i,
                "uuid": self.fake.uuid4(),
                "sender": self.fake.name(),
                "content": self.fake.text(),
                "timestamp": self.fake.date_time(),
                "is_read": self.fake.boolean()
            }
            for i in range(1, n + 1)
        ]


def generate_feedbacks_data(length=Constants.DATA_GENERATION_LENGTH.value):
    return FeedbackGenerator().generate(n=length)
