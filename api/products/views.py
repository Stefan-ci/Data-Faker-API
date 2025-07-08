from fastapi import Request
from utils.viewset import BaseModelViewSet
from utils.base import StateKeywords, Endpoints
from api.products.utils import generate_products_data
from api.products.models import ProductModel, ProductPaginationResponse


class ProductApiView(BaseModelViewSet):
    model = ProductModel
    pagination_model = ProductPaginationResponse
    state_key = StateKeywords.PRODUCTS
    verbose_name = "product"
    verbose_name_plural = "products"
    endpoint_data = Endpoints.PRODUCTS_BASE_ENDPOINT
    generator_func = generate_products_data
    
    def get_data_with_length(self, request: Request, length: int):
        return self.get_accessor(request).get_or_generate(key=self.state_key, func=generate_products_data, length=length)
    
    def regenerate_func(self, request: Request, length: int):
        self.get_accessor(request).set(key=self.state_key, value=generate_products_data(length=length))
