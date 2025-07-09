from utils.base import BaseDataGenerator, Constants


class AttendanceGenerator(BaseDataGenerator):
    def generate(self, n=Constants.DATA_GENERATION_LENGTH.value): # type: ignore
        return [
            {
                "id": i,
                "uuid": self.fake.uuid4(),
                "employee_id": self.fake.uuid4(),
                "check_in": self.fake.date_time_this_decade(),
                "check_out": self.fake.date_time_this_decade(),
                "worked_hours": self.fake.pyfloat(left_digits=2, right_digits=2, positive=True, max_value=24.0),
            }
            for i in range(1, n + 1)
        ]


def generate_attendances_data(length=Constants.DATA_GENERATION_LENGTH.value):
    return AttendanceGenerator().generate(n=length)
