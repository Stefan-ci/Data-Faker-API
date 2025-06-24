from pydantic import Field
from utils.base import CustomBaseModel, CustomPaginationBaseModel

class IncomeModel(CustomBaseModel):
    full_name: str
    company: str
    occupation: str
    country: str
    annual_income: float
    currency: str


class IncomePaginationResponse(CustomPaginationBaseModel):
    """ Response model for paginated Income list """
    results: list[IncomeModel] = Field(default_factory=list)
