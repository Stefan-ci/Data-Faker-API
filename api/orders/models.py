from typing import List
from pydantic import Field
from datetime import datetime
from api.products.models import ProductModel
from utils.base import CustomBaseModel, CustomPaginationBaseModel

class OrderItemModel(CustomBaseModel):
    quantity: int = Field(..., gt=0)
    total: float = Field(..., ge=0)
    product: ProductModel


class OrderModel(CustomBaseModel):
    customer: str
    total: float = Field(..., ge=0)
    date: datetime
    address: str
    order_items: List[OrderItemModel]


class OrderPaginationResponse(CustomPaginationBaseModel):
    """ Response model for paginated order list """
    results: List[OrderModel] = Field(default_factory=list)


class OrderItemPaginationResponse(CustomPaginationBaseModel):
    """ Response model for paginated order items list """
    results: List[OrderItemModel] = Field(default_factory=list)
