from pydantic import Field
from datetime import datetime
from utils.base import CustomBaseModel, CustomPaginationBaseModel

class ChatModel(CustomBaseModel):
    sender: str
    receiver: str
    message: str
    timestamp: datetime
    read: bool = False


class ChatPaginationResponse(CustomPaginationBaseModel):
    """ Response model for paginated chats list """
    results: list[ChatModel] = Field(default_factory=list)
