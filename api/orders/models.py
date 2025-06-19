from typing import List
from pydantic import Field
from datetime import datetime
from api.base import CustomBaseModel
from api.products.models import ProductModel

class OrderItemModel(CustomBaseModel):
    quantity: int = Field(..., gt=0)
    total: float = Field(..., ge=0)
    product: ProductModel


class OrderModel(CustomBaseModel):
    customer: str
    total: float = Field(..., ge=0)
    date: datetime
    order_items: List[OrderItemModel]
