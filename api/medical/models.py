from datetime import date
from api.base import CustomBaseModel

class MedicalDataModel(CustomBaseModel):
    sex: str
    first_name: str
    last_name: str
    blood_type: str
    birth_date: date
    ssn: str
    allergies: str
