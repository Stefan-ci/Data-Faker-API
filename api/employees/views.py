from fastapi import  Request
from utils.viewset import BaseModelViewSet
from utils.base import StateKeywords, Endpoints
from api.employees.utils import generate_employees_data
from api.employees.models import EmployeeModel, EmployeePaginationResponse


class EmployeeApiView(BaseModelViewSet):
    model = EmployeeModel
    pagination_model = EmployeePaginationResponse
    state_key = StateKeywords.EMPLOYEES
    verbose_name = "employee"
    verbose_name_plural = "employees"
    endpoint_data = Endpoints.EMPLOYEES_BASE_ENDPOINT
    generator_func = generate_employees_data
    
    def get_data_with_length(self, request: Request, length: int):
        return self.get_accessor(request).get_or_generate(key=self.state_key, func=generate_employees_data, length=length)
    
    def regenerate_func(self, request: Request, length: int):
        self.get_accessor(request).set(key=self.state_key, value=generate_employees_data(length=length))
