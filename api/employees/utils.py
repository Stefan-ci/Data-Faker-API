from utils.base import BaseDataGenerator, DepartmentChoices


class EmployeeGenerator(BaseDataGenerator):
    def generate(self, n=10): # type: ignore
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
                "salary": round(self.fake.random_int(24_000, 200_000), 2),
            }
            for i in range(1, n + 1)
        ]


def generate_employees_data(length=10):
    return EmployeeGenerator().generate(n=length)
