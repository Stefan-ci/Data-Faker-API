from typing import Optional
from fastapi import  Query, Request, APIRouter, HTTPException

from api.medical.utils import generate_medical_data
from utils.base import StateKeywords, AppStateAccessor
from api.medical.models import MedicalDataModel, MedicalDataPaginationResponse


class MedicalDataApiView:
    def __init__(self):
        self.router = APIRouter(prefix="/medical", tags=["Medical Data"])
        self.router.add_api_route("/", self.list_medical_data, response_model=MedicalDataPaginationResponse, methods=["GET"], summary="List medical data of patients")
        self.router.add_api_route("/{data_id}", self.get_medical_data, response_model=MedicalDataModel, methods=["GET"], summary="Get single patient medical data")
        self.router.add_api_route("/regenerate", self.regenerate_medical_data, methods=["POST"], summary="Regenerate medical data (overwrite the existing ones)")
    
    
    def get_accessor(self, request: Request):
        return AppStateAccessor(request.app.state)
    
    
    async def list_medical_data(
            self,
            request: Request,
            length: Optional[int] = Query(50, ge=1),
            page: Optional[int] = Query(1, ge=1)
        ):
        length = length if length else 50
        page = page if page else 1
        
        medical_data = self.get_accessor(request).get_or_generate(key=StateKeywords.MEDICAL, func=generate_medical_data, length=length)
        all_medical_data_length = len(self.get_accessor(request).get(StateKeywords.MEDICAL)) or 0
        
        if not medical_data:
            raise HTTPException(status_code=503, detail="Medical data is not initialized.")
        
        query_params = dict(request.query_params)
        filterable_fields = MedicalDataModel.get_filterable_fields()
        
        # Dynamic filtering based on query parameters
        for field, value in query_params.items():
            if field in filterable_fields:
                medical_data = [u for u in medical_data if str(u.get(field, "")).casefold() == value.casefold()]
        
        # Pagination logic
        start = (page - 1) * length
        end = start + length
        medical_data = medical_data[start:end]
        
        return MedicalDataPaginationResponse(
            page=page,
            length=length,
            total=all_medical_data_length,
            results=medical_data,
        )
    
    
    async def get_medical_data(self, data_id: str, request: Request):
        medical_data = self.get_accessor(request).get_or_generate(key=StateKeywords.MEDICAL, func=generate_medical_data)
        
        if not medical_data:
            raise HTTPException(status_code=503, detail="Medical data is not initialized.")
        
        data = next((u for u in medical_data if str(u["id"]) == data_id or str(u["uuid"]) == data_id), None)
        if not data:
            raise HTTPException(status_code=404, detail="Medical data not found")
        return data
    
    
    async def regenerate_medical_data(self, request: Request, length: int = Query(100, ge=1)):
        self.get_accessor(request).set(key=StateKeywords.MEDICAL, value=generate_medical_data(length=length))
        return {"message": f"{length} medical data regenerated."}
