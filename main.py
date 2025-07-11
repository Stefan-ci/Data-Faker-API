from fastapi import FastAPI
from typing import List, Type
from contextlib import asynccontextmanager

# utils
from utils.viewset import BaseModelViewSet

# template views
from views.core import router as core_views_router

# API views
from api.users.views import UserApiView
from api.todos.views import TodoApiView
from api.chats.views import ChatApiView
from api.incomes.views import IncomeApiView
from api.expenses.views import ExpenseApiView
from api.products.views import ProductApiView
from api.payments.views import PaymentApiView
from api.analytics.views import AnalyticApiView
from api.employees.views import EmployeeApiView
from api.feedbacks.views import FeedbackApiView
from api.medical.views import MedicalDataApiView
from api.attendances.views import AttendanceApiView
from api.notifications.views import NotificationApiView
from api.orders.views import OrderApiView, OrderItemApiView
from api.cryptos.views import CryptoApiView, CryptoTransactionApiView


@asynccontextmanager
async def on_startup(app: FastAPI):
    # register core routes
    app.include_router(core_views_router)
    
    # register API routes
    api_view_set_classes: List[Type[BaseModelViewSet]] = [
        UserApiView, TodoApiView, ChatApiView, ProductApiView, ExpenseApiView, PaymentApiView, OrderApiView,
        CryptoApiView, IncomeApiView, EmployeeApiView, AnalyticApiView, FeedbackApiView, OrderItemApiView,
        AttendanceApiView, MedicalDataApiView, CryptoTransactionApiView, NotificationApiView
    ]
    
    for ViewSetClass in api_view_set_classes:
        view_set_instance = ViewSetClass()
        app.include_router(view_set_instance.router)
    
    
    # do what you want here
    yield


app = FastAPI(
    title="🧪 Fake Data API",
    description="An API serving fake data. Credits: [Faker](https://faker.readthedocs.io/en/master/). Git repo: [GitHub](https://github.com/Stefan-ci/Data-Faker-API)",
    version="1.0.0",
    lifespan=on_startup,
    debug=True,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}, # Collapse or remove schema section in the docs (too long)
)
