from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.middleware import LocaleMiddleware

# views
from api.users.views import UserApiView
from api.orders.views import OrderApiView
from api.products.views import ProductApiView
from api.employees.views import EmployeeApiView
from api.medical.views import MedicalDataApiView
from api.homepage import router as homepage_router


@asynccontextmanager
async def on_startup(app: FastAPI):
    # init some data here if you want to.
    # I just want to keep the main file very simple
    yield


app = FastAPI(
    title="🧪 Fake Data API",
    description="An API serving fake data.",
    version="1.0.0",
    lifespan=on_startup,
    debug=True
)

# middlewares
app.add_middleware(LocaleMiddleware)


# Include API routes
app.include_router(homepage_router)

app.include_router(UserApiView().router)
app.include_router(OrderApiView().router)
app.include_router(ProductApiView().router)
app.include_router(EmployeeApiView().router)
app.include_router(MedicalDataApiView().router)
