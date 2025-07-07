from fastapi import  Request
from utils.viewset import BaseModelViewSet
from utils.base import StateKeywords, Endpoints
from api.payments.utils import generate_payments_data
from api.payments.models import PaymentModel, PaymentPaginationResponse


class PaymentApiView(BaseModelViewSet):
    model = PaymentModel
    pagination_model = PaymentPaginationResponse
    state_key = StateKeywords.PAYMENTS
    verbose_name = "payment"
    verbose_name_plural = "payments"
    endpoint_prefix = Endpoints.PAYMENTS_BASE_ENDPOINT.endpoint
    
    def get_data_with_length(self, request: Request, length: int):
        return self.get_accessor(request).get_or_generate(key=self.state_key, func=generate_payments_data, length=length)
    
    def regenerate_func(self, request: Request, length: int):
        self.get_accessor(request).set(key=self.state_key, value=generate_payments_data(length=length))
