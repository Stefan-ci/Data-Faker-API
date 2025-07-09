from utils.base import BaseDataGenerator, Constants


class ExpenseModelGenerator(BaseDataGenerator):
    def generate(self, n=Constants.DATA_GENERATION_LENGTH.value): # type: ignore
        categories = ["Food", "Transport", "Rent", "Utilities", "Entertainment"]
        labels = ["Grocery", "Taxi", "Internet", "Movie", "Electricity", "Water Bill", "Subscription"]
        
        return [
            {
                "id": i,
                "uuid": self.fake.uuid4(),
                "label": self.fake.random_element(labels),
                "category": self.fake.random_element(categories),
                "amount": self.fake.pyfloat(left_digits=7, right_digits=2, min_value=1, max_value=9_999.99),
                "date": self.fake.date(),
            }
            for i in range(1, n + 1)
        ]


def generate_expenses_data(length=Constants.DATA_GENERATION_LENGTH.value):
    return ExpenseModelGenerator().generate(n=length)
