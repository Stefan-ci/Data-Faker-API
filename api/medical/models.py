from datetime import date
from pydantic import Field
from utils.base import CustomBaseModel, CustomPaginationBaseModel

class MedicalDataModel(CustomBaseModel):
    sex: str
    first_name: str
    last_name: str
    blood_type: str
    birth_date: date
    ssn: str
    allergies: str


class MedicalDataPaginationResponse(CustomPaginationBaseModel):
    """ Response model for paginated medical data list """
    results: list[MedicalDataModel] = Field(default_factory=list)
