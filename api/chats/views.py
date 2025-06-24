from fastapi import  Request
from utils.base import StateKeywords
from utils.viewset import BaseModelViewSet
from api.chats.utils import generate_chats_data
from api.chats.models import ChatModel, ChatPaginationResponse


class ChatApiView(BaseModelViewSet):
    model = ChatModel
    pagination_model = ChatPaginationResponse
    state_key = StateKeywords.CHATS
    verbose_name = "chat"
    verbose_name_plural = "chats"
    endpoint_prefix = "/chats"
    
    def get_data_with_length(self, request: Request, length: int):
        return self.get_accessor(request).get_or_generate(key=self.state_key, func=generate_chats_data, length=length)
    
    def regenerate_func(self, request: Request, length: int):
        self.get_accessor(request).set(key=self.state_key, value=generate_chats_data(length=length))
