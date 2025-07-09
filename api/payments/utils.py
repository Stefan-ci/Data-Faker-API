from utils.base import BaseDataGenerator, Constants


class PaymentGenerator(BaseDataGenerator):
    def generate(self, n=Constants.DATA_GENERATION_LENGTH.value): # type: ignore
        methods = ["Cash", "Credit Card", "Debit Card", "Bank Transfer", "PayPal", "Cryptocurrency", "Mobile Payment"]
        statuses = ["Pending", "Completed", "Failed", "Refunded"]
        
        return [
            {
                "id": i,
                "uuid": self.fake.uuid4(),
                "hash": self.fake.sha256(),
                "amount": self.fake.pyfloat(left_digits=7, right_digits=2, min_value=1, max_value=9_999.99),
                "date": self.fake.date(),
                "status": self.fake.random_element(statuses),
                "method": self.fake.random_element(methods),
            }
            for i in range(1, n + 1)
        ]


def generate_payments_data(length=Constants.DATA_GENERATION_LENGTH.value):
    return PaymentGenerator().generate(n=length)
