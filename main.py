from fastapi import FastAPI
from contextlib import asynccontextmanager

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
    # init some data here if you want to.
    # I just want to keep the main file very simple
    yield


app = FastAPI(
    title="🧪 Fake Data API",
    description="An API serving fake data. Credits: [Faker](https://faker.readthedocs.io/en/master/). Git repo: [GitHub](https://github.com/Stefan-ci/Data-Faker-API)",
    version="1.0.0",
    lifespan=on_startup,
    debug=True,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}, # Collapse or remove schema section in the docs (too long)
)

# Core routes
app.include_router(core_views_router)

# Include API routes
app.include_router(UserApiView().router)
app.include_router(TodoApiView().router)
app.include_router(ChatApiView().router)
app.include_router(OrderApiView().router)
app.include_router(CryptoApiView().router)
app.include_router(IncomeApiView().router)
app.include_router(ProductApiView().router)
app.include_router(ExpenseApiView().router)
app.include_router(PaymentApiView().router)
app.include_router(EmployeeApiView().router)
app.include_router(AnalyticApiView().router)
app.include_router(FeedbackApiView().router)
app.include_router(OrderItemApiView().router)
app.include_router(AttendanceApiView().router)
app.include_router(MedicalDataApiView().router)
app.include_router(NotificationApiView().router)
app.include_router(CryptoTransactionApiView().router)
