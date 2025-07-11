from utils.base import BaseDataGenerator, Constants


class TodoGenerator(BaseDataGenerator):
    def generate(self, n=Constants.DATA_GENERATION_LENGTH.value): # type: ignore
        priorities = ["low", "medium", "high"]
        statuses = ["pending", "in progress", "completed"]
        
        return [
            {
                "id": i,
                "uuid": self.fake.uuid4(),
                "title": self.fake.sentence(),
                "description": self.fake.paragraph(),
                "due_date": self.fake.date_between(start_date="today", end_date="+30d"),
                "priority": self.fake.random_element(priorities),
                "status": self.fake.random_element(statuses),
                "assignee": self.fake.name()
            }
            for i in range(1, n + 1)
        ]


def generate_todos_data(length=Constants.DATA_GENERATION_LENGTH.value):
    return TodoGenerator().generate(n=length)
