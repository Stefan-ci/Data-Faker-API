from fastapi import  Request
from utils.viewset import BaseModelViewSet
from utils.base import StateKeywords, Endpoints
from api.todos.utils import generate_todos_data
from api.todos.models import TodoModel, TodoPaginationResponse


class TodoApiView(BaseModelViewSet):
    model = TodoModel
    pagination_model = TodoPaginationResponse
    state_key = StateKeywords.TODOS
    verbose_name = "todo"
    verbose_name_plural = "todos"
    endpoint_data = Endpoints.TODOS_BASE_ENDPOINT
    generator_func = generate_todos_data
    
    def get_data_with_length(self, request: Request, length: int):
        return self.get_accessor(request).get_or_generate(key=self.state_key, func=generate_todos_data, length=length)
    
    def regenerate_func(self, request: Request, length: int):
        self.get_accessor(request).set(key=self.state_key, value=generate_todos_data(length=length))
