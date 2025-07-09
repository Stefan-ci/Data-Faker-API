from utils.base import BaseDataGenerator, Constants


class NotificationGenerator(BaseDataGenerator):
    def generate(self, n=Constants.DATA_GENERATION_LENGTH.value): # type: ignore
        levels = ["info", "success", "warning", "error"]
        
        return [
            {
                "id": i,
                "uuid": self.fake.uuid4(),
                "title": self.fake.sentence(),
                "message": self.fake.text(max_nb_chars=200),
                "level": self.fake.random_element(levels),
                "timestamp": self.fake.date_time_this_decade(),
                "is_read": self.fake.boolean(),
            }
            for i in range(1, n + 1)
        ]


def generate_notifications_data(length=Constants.DATA_GENERATION_LENGTH.value):
    return NotificationGenerator().generate(n=length)
