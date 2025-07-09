from utils.base import BaseDataGenerator, DepartmentChoices, Constants


class EmployeeGenerator(BaseDataGenerator):
    def generate(self, n=Constants.DATA_GENERATION_LENGTH.value): # type: ignore
        return [
            {
                "id": i,
                "uuid": self.fake.uuid4(),
                "first_name": self.fake.first_name(),
                "last_name": self.fake.last_name(),
                "email": self.fake.email(),
                "phone_number": self.fake.phone_number(),
                "job_title": self.fake.job(),
                "hire_date": self.fake.date_of_birth(minimum_age=0, maximum_age=90).isoformat(),
                "department": self.fake.random_element([dept.value for dept in DepartmentChoices]),
                "salary": self.fake.pyfloat(left_digits=7, right_digits=2, min_value=24_000, max_value=300_00),
            }
            for i in range(1, n + 1)
        ]


def generate_employees_data(length=Constants.DATA_GENERATION_LENGTH.value):
    return EmployeeGenerator().generate(n=length)
