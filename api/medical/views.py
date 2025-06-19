from typing import Optional, List
from fastapi import  Query, Request, APIRouter, HTTPException

from api.medical.models import MedicalDataModel
from api.medical.utils import generate_medical_data
from api.base import StateKeywords, AppStateAccessor


class MedicalDataApiView:
    def __init__(self):
        self.router = APIRouter(prefix="/medical", tags=["Medical Data"])
        self.router.add_api_route("/", self.list_medical_data, response_model=List[MedicalDataModel], methods=["GET"], summary="List medical data of patients")
        self.router.add_api_route("/{data_id}", self.get_medical_data, response_model=MedicalDataModel, methods=["GET"], summary="Get single patient medical data")
        self.router.add_api_route("/regenerate", self.regenerate_medical_data, methods=["POST"], summary="Regenerate medical data (overwrite the existing ones)")
    
    
    def get_accessor(self, request: Request):
        return AppStateAccessor(request.app.state)
    
    
    async def list_medical_data(
            self,
            request: Request,
            length: Optional[int] = Query(50, ge=1)
        ):
        length = length if length else 50
        medical_data = self.get_accessor(request).get_or_generate(key=StateKeywords.MEDICAL, func=generate_medical_data, length=length)
        return medical_data
    
    
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
