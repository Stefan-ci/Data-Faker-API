from typing import Optional
from fastapi import  Query, Request, APIRouter, HTTPException

from api.base import StateKeywords, AppStateAccessor
from api.employees.utils import generate_employees_data
from api.employees.models import EmployeeModel, EmployeePaginationResponse


class EmployeeApiView:
    def __init__(self):
        self.router = APIRouter(prefix="/employees", tags=["Employees"])
        self.router.add_api_route("/", self.list_employees, response_model=EmployeePaginationResponse, methods=["GET"], summary="List employees")
        self.router.add_api_route("/{employee_id}", self.get_employee, response_model=EmployeeModel, methods=["GET"], summary="Get single employee")
        self.router.add_api_route("/regenerate", self.regenerate_employees, methods=["POST"], summary="Regenerate employees (overwrite the existing ones)")
    
    
    def get_accessor(self, request: Request):
        return AppStateAccessor(request.app.state)
    
    
    async def list_employees(
            self,
            request: Request,
            length: Optional[int] = Query(50, ge=1),
            page: Optional[int] = Query(1, ge=1)
        ):
        length = length if length else 50
        page = page if page else 1
        
        employees = self.get_accessor(request).get_or_generate(key=StateKeywords.EMPLOYEES, func=generate_employees_data, length=length)
        all_employees_length = len(self.get_accessor(request).get(StateKeywords.EMPLOYEES)) or 0
        
        if not employees:
            raise HTTPException(status_code=503, detail="Employees data is not initialized.")
        
        query_params = dict(request.query_params)
        filterable_fields = EmployeeModel.get_filterable_fields()
        
        # Dynamic filtering based on query parameters
        for field, value in query_params.items():
            if field in filterable_fields:
                employees = [u for u in employees if str(u.get(field, "")).casefold() == value.casefold()]
        
        # Pagination logic
        start = (page - 1) * length
        end = start + length
        employees = employees[start:end]

        return EmployeePaginationResponse(
            page=page,
            length=length,
            total=all_employees_length,
            results=employees,
        )
    
    
    async def get_employee(self, employee_id: str, request: Request):
        employees = self.get_accessor(request).get_or_generate(key=StateKeywords.EMPLOYEES, func=generate_employees_data)
        
        if not employees:
            raise HTTPException(status_code=503, detail="Employees data is not initialized.")
        
        employee = next((u for u in employees if str(u["id"]) == employee_id or str(u["uuid"]) == employee_id), None)
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        return employee
    
    
    async def regenerate_employees(self, request: Request, length: int = Query(100, ge=1)):
        self.get_accessor(request).set(key=StateKeywords.EMPLOYEES, value=generate_employees_data(length=length))
        return {"message": f"{length} employees regenerated."}
