from datetime import date
from pydantic import Field
from api.base import CustomBaseModel, CustomPaginationBaseModel

class EmployeeModel(CustomBaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    job_title: str
    hire_date: date
    department: str
    salary: float


class EmployeePaginationResponse(CustomPaginationBaseModel):
    """ Response model for paginated employee list """
    results: list[EmployeeModel] = Field(default_factory=list)
