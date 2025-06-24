from fastapi import Request
from utils.base import StateKeywords
from utils.viewset import BaseModelViewSet
from api.users.utils import generate_users_data
from api.users.models import UserModel, UserPaginationResponse


class UserApiView(BaseModelViewSet):
    model = UserModel
    pagination_model = UserPaginationResponse
    state_key = StateKeywords.USERS
    verbose_name = "user"
    verbose_name_plural = "users"
    endpoint_prefix = "/users"
    
    def get_data_with_length(self, request: Request, length: int):
        return self.get_accessor(request).get_or_generate(key=self.state_key, func=generate_users_data, length=length)
    
    def regenerate_func(self, request: Request, length: int):
        self.get_accessor(request).set(key=self.state_key, value=generate_users_data(length=length))
