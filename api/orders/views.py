from fastapi import Request
from utils.base import StateKeywords
from utils.viewset import BaseModelViewSet
from api.orders.utils import generate_orders_data
from api.orders.models import OrderModel, OrderPaginationResponse


class OrderApiView(BaseModelViewSet):
    model = OrderModel
    pagination_model = OrderPaginationResponse
    state_key = StateKeywords.ORDERS
    verbose_name = "order"
    verbose_name_plural = "orders"
    endpoint_prefix = "/orders"
    
    def get_data_with_length(self, request: Request, length: int):
        return self.get_accessor(request).get_or_generate(key=self.state_key, func=generate_orders_data, length=length)
    
    def regenerate_func(self, request: Request, length: int):
        self.get_accessor(request).set(key=self.state_key, value=generate_orders_data(length=length))
