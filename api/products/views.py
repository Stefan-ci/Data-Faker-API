from typing import Optional, List
from fastapi import  Query, Request, APIRouter, HTTPException

from api.products.models import ProductModel
from api.base import StateKeywords, AppStateAccessor
from api.products.utils import generate_products_data


class ProductApiView:
    def __init__(self):
        self.router = APIRouter(prefix="/products", tags=["Products"])
        self.router.add_api_route("/", self.list_products, response_model=List[ProductModel], methods=["GET"], summary="List products")
        self.router.add_api_route("/{product_id}", self.get_product, response_model=ProductModel, methods=["GET"], summary="Get single product")
        self.router.add_api_route("/regenerate", self.regenerate_products, methods=["POST"], summary="Regenerate products (overwrite the existing ones)")
    
    
    def get_accessor(self, request: Request):
        return AppStateAccessor(request.app.state)
    
    
    async def list_products(
            self,
            request: Request,
            length: Optional[int] = Query(50, ge=1)
        ):
        length = length if length else 50
        accessor = self.get_accessor(request)
        locale = accessor.get(StateKeywords.LOCALE_LANG) or "en_US"
        products = accessor.get_or_generate(key=StateKeywords.PRODUCTS, func=generate_products_data, length=length, locale=locale)
        return products
    
    
    async def get_product(self, product_id: str, request: Request):
        accessor = self.get_accessor(request)
        locale = accessor.get(StateKeywords.LOCALE_LANG) or "en_US"
        products = accessor.get_or_generate(key=StateKeywords.PRODUCTS, func=generate_products_data, locale=locale)
        
        if not products:
            raise HTTPException(status_code=503, detail="Products data is not initialized.")
        
        product = next((u for u in products if str(u["id"]) == product_id or str(u["uuid"]) == product_id), None)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    
    
    async def regenerate_products(self, request: Request, length: int = Query(100, ge=1)):
        accessor = self.get_accessor(request)
        locale = accessor.get(StateKeywords.LOCALE_LANG) or "en_US"
        accessor.set(key=StateKeywords.PRODUCTS, value=generate_products_data(length=length, locale=locale))
        return {"message": f"{length} products regenerated."}
