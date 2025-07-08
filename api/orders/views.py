from fastapi import Request
from utils.viewset import BaseModelViewSet
from utils.base import StateKeywords, Endpoints
from api.orders.utils import generate_orders_data, generate_order_items_data
from api.orders.models import OrderModel, OrderPaginationResponse, OrderItemModel, OrderItemPaginationResponse


class OrderApiView(BaseModelViewSet):
    model = OrderModel
    pagination_model = OrderPaginationResponse
    state_key = StateKeywords.ORDERS
    verbose_name = "order"
    verbose_name_plural = "orders"
    endpoint_data = Endpoints.ORDERS_BASE_ENDPOINT
    generator_func = generate_orders_data
    
    def get_data_with_length(self, request: Request, length: int):
        return self.get_accessor(request).get_or_generate(key=self.state_key, func=generate_orders_data, length=length)
    
    def regenerate_func(self, request: Request, length: int):
        self.get_accessor(request).set(key=self.state_key, value=generate_orders_data(length=length))



class OrderItemApiView(BaseModelViewSet):
    model = OrderItemModel
    pagination_model = OrderItemPaginationResponse
    state_key = StateKeywords.ORDER_ITEMS
    verbose_name = "order item"
    verbose_name_plural = "orders items"
    endpoint_data = Endpoints.ORDER_ITEMS_BASE_ENDPOINT
    tags = "Order items"
    generator_func = generate_order_items_data
    
    def get_data_with_length(self, request: Request, length: int):
        return self.get_accessor(request).get_or_generate(key=self.state_key, func=generate_order_items_data, length=length)
    
    def regenerate_func(self, request: Request, length: int):
        self.get_accessor(request).set(key=self.state_key, value=generate_order_items_data(length=length))
