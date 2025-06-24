from pydantic import Field
from datetime import datetime
from utils.base import CustomBaseModel, CustomPaginationBaseModel

class NotificationModel(CustomBaseModel):
    title: str
    message: str
    level: str
    timestamp: datetime
    is_read: bool


class NotificationPaginationResponse(CustomPaginationBaseModel):
    """ Response model for paginated Notification list """
    results: list[NotificationModel] = Field(default_factory=list)
