from fastapi import  Request
from utils.viewset import BaseModelViewSet
from utils.base import StateKeywords, Endpoints
from api.analytics.utils import generate_analytics_data
from api.analytics.models import AnalyticModel, AnalyticPaginationResponse


class AnalyticApiView(BaseModelViewSet):
    model = AnalyticModel
    pagination_model = AnalyticPaginationResponse
    state_key = StateKeywords.ANALYTICS
    verbose_name = "analytic"
    verbose_name_plural = "analytics"
    endpoint_prefix = Endpoints.ANALYTICS_BASE_ENDPOINT.endpoint
    generator_func = generate_analytics_data
    
    def get_data_with_length(self, request: Request, length: int):
        return self.get_accessor(request).get_or_generate(key=self.state_key, func=generate_analytics_data, length=length)
    
    def regenerate_func(self, request: Request, length: int):
        self.get_accessor(request).set(key=self.state_key, value=generate_analytics_data(length=length))
