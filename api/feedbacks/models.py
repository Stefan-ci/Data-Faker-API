from pydantic import Field
from datetime import datetime
from utils.base import CustomBaseModel, CustomPaginationBaseModel

class FeedbackModel(CustomBaseModel):
    sender: str
    content: str
    timestamp: datetime
    is_read: bool = False


class FeedbackPaginationResponse(CustomPaginationBaseModel):
    """ Response model for paginated feedbacks list """
    results: list[FeedbackModel] = Field(default_factory=list)
