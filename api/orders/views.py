from typing import Optional, List
from fastapi import  Query, Request, APIRouter, HTTPException

from api.orders.models import OrderModel
from api.orders.utils import generate_orders_data
from api.base import StateKeywords, AppStateAccessor


class OrderApiView:
    def __init__(self):
        self.router = APIRouter(prefix="/orders", tags=["Orders"])
        self.router.add_api_route("/", self.list_orders, response_model=List[OrderModel], methods=["GET"], summary="List orders")
        self.router.add_api_route("/{order_id}", self.get_order, response_model=OrderModel, methods=["GET"], summary="Get single order")
        self.router.add_api_route("/regenerate", self.regenerate_orders, methods=["POST"], summary="Regenerate orders (overwrite the existing ones)")
    
    
    def get_accessor(self, request: Request):
        return AppStateAccessor(request.app.state)
    
    
    async def list_orders(
            self,
            request: Request,
            length: Optional[int] = Query(10, ge=1)
        ):
        length = length if length else 10
        orders = self.get_accessor(request).get_or_generate(key=StateKeywords.ORDERS, func=generate_orders_data, length=length)
        return orders
    
    
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
