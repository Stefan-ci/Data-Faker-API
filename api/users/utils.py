from api.base import BaseDataGenerator, SexChoices


class UserGenerator(BaseDataGenerator):
    def generate(self, n=10): # type: ignore
        return [
            {
                "id": i,
                "uuid": self.fake.uuid4(),
                "first_name": self.fake.first_name(),
                "last_name": self.fake.last_name(),
                "email": self.fake.email(),
                "username": self.fake.user_name(),
                "phone_number": self.fake.phone_number(),
                "birth_date": self.fake.date_of_birth(minimum_age=0, maximum_age=90).isoformat(),
                "sex": self.fake.random_element([sex.value for sex in SexChoices]),
                "address": self.fake.address(),
                "postal_code": self.fake.postalcode(),
                "city": self.fake.city(),
                "country": self.fake.country(),
                "date_joined": self.fake.date_time().isoformat(),
                "last_login": self.fake.date_time().isoformat(),
                "is_active": self.fake.boolean(),
                "is_staff": self.fake.boolean(),
                "is_superuser": self.fake.boolean(),
            }
            for i in range(1, n + 1)
        ]


def generate_users_data(length=10):
    return UserGenerator().generate(n=length)
