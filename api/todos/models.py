from datetime import date
from pydantic import Field
from utils.base import CustomBaseModel, CustomPaginationBaseModel

class TodoModel(CustomBaseModel):
    title: str
    description: str
    due_date: date
    priority: str
    status: str
    assignee: str


class TodoPaginationResponse(CustomPaginationBaseModel):
    """ Response model for paginated todos list """
    results: list[TodoModel] = Field(default_factory=list)
