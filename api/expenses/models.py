from datetime import date
from pydantic import Field
from utils.base import CustomBaseModel, CustomPaginationBaseModel

class ExpenseModel(CustomBaseModel):
    label: str
    category: str
    amount: float
    date: date



class ExpensePaginationResponse(CustomPaginationBaseModel):
    """ Response model for paginated Expense list """
    results: list[ExpenseModel] = Field(default_factory=list)
