from fastapi import  Request
from utils.viewset import BaseModelViewSet
from utils.base import StateKeywords, Endpoints
from api.notifications.utils import generate_notifications_data
from api.notifications.models import NotificationModel, NotificationPaginationResponse


class NotificationApiView(BaseModelViewSet):
    model = NotificationModel
    pagination_model = NotificationPaginationResponse
    state_key = StateKeywords.NOTIFICATIONS
    verbose_name = "notification"
    verbose_name_plural = "notifications"
    endpoint_prefix = Endpoints.NOTIFICATIONS_BASE_ENDPOINT.endpoint
    
    def get_data_with_length(self, request: Request, length: int):
        return self.get_accessor(request).get_or_generate(key=self.state_key, func=generate_notifications_data, length=length)
    
    def regenerate_func(self, request: Request, length: int):
        self.get_accessor(request).set(key=self.state_key, value=generate_notifications_data(length=length))
