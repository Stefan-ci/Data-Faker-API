from fastapi import Request
from utils.viewset import BaseModelViewSet
from utils.base import StateKeywords,  Endpoints
from api.incomes.utils import generate_incomes_data
from api.incomes.models import IncomeModel, IncomePaginationResponse


class IncomeApiView(BaseModelViewSet):
    model = IncomeModel
    pagination_model = IncomePaginationResponse
    state_key = StateKeywords.INCOMES
    verbose_name = "income"
    verbose_name_plural = "incomes"
    endpoint_data = Endpoints.INCOMES_BASE_ENDPOINT
    generator_func = generate_incomes_data
    
    def get_data_with_length(self, request: Request, length: int):
        return self.get_accessor(request).get_or_generate(key=self.state_key, func=generate_incomes_data, length=length)
    
    def regenerate_func(self, request: Request, length: int):
        self.get_accessor(request).set(key=self.state_key, value=generate_incomes_data(length=length))
