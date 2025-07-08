from fastapi import  Request
from utils.viewset import BaseModelViewSet
from utils.base import StateKeywords, Endpoints
from api.attendances.utils import generate_attendances_data
from api.attendances.models import AttendanceModel, AttendancePaginationResponse


class AttendanceApiView(BaseModelViewSet):
    model = AttendanceModel
    pagination_model = AttendancePaginationResponse
    state_key = StateKeywords.ATTENDANCES
    verbose_name = "attendance"
    verbose_name_plural = "attendances"
    endpoint_data = Endpoints.ATTENDANCES_BASE_ENDPOINT
    generator_func = generate_attendances_data
    
    def get_data_with_length(self, request: Request, length: int):
        return self.get_accessor(request).get_or_generate(key=self.state_key, func=generate_attendances_data, length=length)
    
    def regenerate_func(self, request: Request, length: int):
        self.get_accessor(request).set(key=self.state_key, value=generate_attendances_data(length=length))
