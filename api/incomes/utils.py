from utils.base import BaseDataGenerator, Constants


class IncomeModelGenerator(BaseDataGenerator):
    def generate(self, n=Constants.DATA_GENERATION_LENGTH.value): # type: ignore
        return [
            {
                "id": i,
                "uuid": self.fake.uuid4(),
                "full_name": self.fake.name(),
                "company": self.fake.company(),
                "occupation": self.fake.job(),
                "country": self.fake.country(),
                "annual_income": self.fake.pyfloat(left_digits=7, right_digits=2, min_value=50_000, max_value=9_999_999),
                "currency": f"{self.fake.currency_name()} ({self.fake.currency_code()})",
            }
            for i in range(1, n + 1)
        ]


def generate_incomes_data(length=Constants.DATA_GENERATION_LENGTH.value):
    return IncomeModelGenerator().generate(n=length)
