from fastapi import  Request
from utils.base import StateKeywords
from utils.viewset import BaseModelViewSet
from api.medical.utils import generate_medical_data
from api.medical.models import MedicalDataModel, MedicalDataPaginationResponse


class MedicalDataApiView(BaseModelViewSet):
    model = MedicalDataModel
    pagination_model = MedicalDataPaginationResponse
    state_key = StateKeywords.MEDICAL
    verbose_name = "medical"
    verbose_name_plural = "medicals"
    endpoint_prefix = "/medical"
    
    def get_data_with_length(self, request: Request, length: int):
        return self.get_accessor(request).get_or_generate(key=self.state_key, func=generate_medical_data, length=length)
    
    def regenerate_func(self, request: Request, length: int):
        self.get_accessor(request).set(key=self.state_key, value=generate_medical_data(length=length))
