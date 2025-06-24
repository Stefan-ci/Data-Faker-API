from datetime import date
from pydantic import Field
from utils.base import CustomBaseModel, CustomPaginationBaseModel

class PaymentModel(CustomBaseModel):
    hash: str
    amount: float
    date: date
    status: str
    method: str


class PaymentPaginationResponse(CustomPaginationBaseModel):
    """ Response model for paginated Payment list """
    results: list[PaymentModel] = Field(default_factory=list)
