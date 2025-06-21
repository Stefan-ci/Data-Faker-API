from typing import Optional
from fastapi import  Query, Request, APIRouter, HTTPException

from utils.base import StateKeywords, AppStateAccessor
from api.products.utils import generate_products_data
from api.products.models import ProductModel, ProductPaginationResponse


class ProductApiView:
    def __init__(self):
        self.router = APIRouter(prefix="/products", tags=["Products"])
        self.router.add_api_route("/", self.list_products, response_model=ProductPaginationResponse, methods=["GET"], summary="List products")
        self.router.add_api_route("/{product_id}", self.get_product, response_model=ProductModel, methods=["GET"], summary="Get single product")
        self.router.add_api_route("/regenerate", self.regenerate_products, methods=["POST"], summary="Regenerate products (overwrite the existing ones)")
    
    
    def get_accessor(self, request: Request):
        return AppStateAccessor(request.app.state)
    
    
    async def list_products(
            self,
            request: Request,
            length: Optional[int] = Query(50, ge=1),
            page: Optional[int] = Query(1, ge=1)
        ):
        length = length if length else 50
        page = page if page else 1
        
        products = self.get_accessor(request).get_or_generate(key=StateKeywords.PRODUCTS, func=generate_products_data, length=length)
        all_products_length = len(self.get_accessor(request).get(StateKeywords.PRODUCTS)) or 0
        
        if not products:
            raise HTTPException(status_code=503, detail="Products data is not initialized.")
        
        query_params = dict(request.query_params)
        filterable_fields = ProductModel.get_filterable_fields()
        
        # Dynamic filtering based on query parameters
        for field, value in query_params.items():
            if field in filterable_fields:
                products = [u for u in products if str(u.get(field, "")).casefold() == value.casefold()]
        
        # Pagination logic
        start = (page - 1) * length
        end = start + length
        products = products[start:end]
        
        return ProductPaginationResponse(
            page=page,
            length=length,
            total=all_products_length,
            results=products,
        )
    
    
    async def get_product(self, product_id: str, request: Request):
        products = self.get_accessor(request).get_or_generate(key=StateKeywords.PRODUCTS, func=generate_products_data)
        
        if not products:
            raise HTTPException(status_code=503, detail="Products data is not initialized.")
        
        product = next((u for u in products if str(u["id"]) == product_id or str(u["uuid"]) == product_id), None)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    
    
    async def regenerate_products(self, request: Request, length: int = Query(100, ge=1)):
        self.get_accessor(request).set(key=StateKeywords.PRODUCTS, value=generate_products_data(length=length))
        return {"message": f"{length} products regenerated."}
