from api.base import BaseDataGenerator, SexChoices, AllergiesChoices


class MedicalGenerator(BaseDataGenerator):
    def generate(self, n=10): # type: ignore
        return [
            {
                "id": i,
                "uuid": self.fake.uuid4(),
                "sex": self.fake.random_element([sex.value for sex in SexChoices]),
                "first_name": self.fake.first_name(),
                "last_name": self.fake.last_name(),
                "blood_type": self.fake.random_element(["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]),
                "birth_date": self.fake.date_of_birth(minimum_age=0, maximum_age=90).isoformat(),
                "ssn": self.fake.ssn(),
                "allergies": self.fake.word(ext_word_list=[allergy.value for allergy in AllergiesChoices]),
            }
            for i in range(1, n + 1)
        ]


def generate_medical_data(length=10):
    return MedicalGenerator().generate(n=length)
