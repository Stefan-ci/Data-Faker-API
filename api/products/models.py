from pydantic import Field
from datetime import datetime
from api.base import CustomBaseModel

class ProductModel(CustomBaseModel):
    name: str
    category: str
    price: float
    ean_13: str
    stock:  int = Field(..., ge=0)
    vendor: str
    picture: str
    description: str
    rating: float
    reviews_count: int
    created_at: datetime
