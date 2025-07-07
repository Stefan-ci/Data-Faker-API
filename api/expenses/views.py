from fastapi import Request
from utils.viewset import BaseModelViewSet
from utils.base import StateKeywords, Endpoints
from api.expenses.utils import generate_expenses_data
from api.expenses.models import ExpenseModel, ExpensePaginationResponse


class ExpenseApiView(BaseModelViewSet):
    model = ExpenseModel
    pagination_model = ExpensePaginationResponse
    state_key = StateKeywords.EXPENSES
    verbose_name = "expense"
    verbose_name_plural = "expenses"
    endpoint_prefix = Endpoints.EXPENSES_BASE_ENDPOINT.endpoint
    generator_func = generate_expenses_data
    
    def get_data_with_length(self, request: Request, length: int):
        return self.get_accessor(request).get_or_generate(key=self.state_key, func=generate_expenses_data, length=length)
    
    def regenerate_func(self, request: Request, length: int):
        self.get_accessor(request).set(key=self.state_key, value=generate_expenses_data(length=length))
