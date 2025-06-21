from typing import Optional
from fastapi import  Query, Request, APIRouter, HTTPException

from api.orders.utils import generate_orders_data
from utils.base import StateKeywords, AppStateAccessor
from api.orders.models import OrderModel, OrderPaginationResponse


class OrderApiView:
    def __init__(self):
        self.router = APIRouter(prefix="/orders", tags=["Orders"])
        self.router.add_api_route("/", self.list_orders, response_model=OrderPaginationResponse, methods=["GET"], summary="List orders")
        self.router.add_api_route("/{order_id}", self.get_order, response_model=OrderModel, methods=["GET"], summary="Get single order")
        self.router.add_api_route("/regenerate", self.regenerate_orders, methods=["POST"], summary="Regenerate orders (overwrite the existing ones)")
    
    
    def get_accessor(self, request: Request):
        return AppStateAccessor(request.app.state)
    
    
    async def list_orders(
            self,
            request: Request,
            length: Optional[int] = Query(10, ge=1),
            page: Optional[int] = Query(1, ge=1)
        ):
        length = length if length else 10
        page = page if page else 1
        
        orders = self.get_accessor(request).get_or_generate(key=StateKeywords.ORDERS, func=generate_orders_data, length=length)
        all_orders_length = len(self.get_accessor(request).get(StateKeywords.ORDERS)) or 0
        
        if not orders:
            raise HTTPException(status_code=503, detail="Orders data is not initialized.")
        
        query_params = dict(request.query_params)
        filterable_fields = OrderModel.get_filterable_fields()
        
        # Dynamic filtering based on query parameters
        for field, value in query_params.items():
            if field in filterable_fields:
                orders = [u for u in orders if str(u.get(field, "")).casefold() == value.casefold()]
        
        # Pagination logic
        start = (page - 1) * length
        end = start + length
        orders = orders[start:end]
        
        return OrderPaginationResponse(
            page=page,
            length=length,
            total=all_orders_length,
            results=orders,
        )
    
    
    async def get_order(self, order_id: str, request: Request):
        orders = self.get_accessor(request).get_or_generate(key=StateKeywords.ORDERS, func=generate_orders_data)
        
        if not orders:
            raise HTTPException(status_code=503, detail="Orders data is not initialized.")
        
        order = next((u for u in orders if str(u["id"]) == order_id or str(u["uuid"]) == order_id), None)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    
    
    async def regenerate_orders(self, request: Request, length: int = Query(100, ge=1)):
        self.get_accessor(request).set(key=StateKeywords.ORDERS, value=generate_orders_data(length=length))
        return {"message": f"{length} orders regenerated."}
