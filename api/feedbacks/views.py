from fastapi import  Request
from utils.viewset import BaseModelViewSet
from utils.base import StateKeywords, Endpoints
from api.feedbacks.utils import generate_feedbacks_data
from api.feedbacks.models import FeedbackModel, FeedbackPaginationResponse


class FeedbackApiView(BaseModelViewSet):
    model = FeedbackModel
    pagination_model = FeedbackPaginationResponse
    state_key = StateKeywords.FEEDBACKS
    verbose_name = "feedback"
    verbose_name_plural = "feedbacks"
    endpoint_data = Endpoints.FEEDBACKS_BASE_ENDPOINT
    generator_func = generate_feedbacks_data
    
    def get_data_with_length(self, request: Request, length: int):
        return self.get_accessor(request).get_or_generate(key=self.state_key, func=generate_feedbacks_data, length=length)
    
    def regenerate_func(self, request: Request, length: int):
        self.get_accessor(request).set(key=self.state_key, value=generate_feedbacks_data(length=length))
