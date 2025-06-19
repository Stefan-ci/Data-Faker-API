from datetime import date
from api.base import CustomBaseModel

class EmployeeModel(CustomBaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    job_title: str
    hire_date: date
    department: str
    salary: float
