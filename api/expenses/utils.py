from utils.base import BaseDataGenerator


class ExpenseModelGenerator(BaseDataGenerator):
    def generate(self, n=10): # type: ignore
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


def generate_expenses_data(length=10):
    return ExpenseModelGenerator().generate(n=length)
