from abc import ABC, abstractmethod
from typing import Type, Optional, Callable
from fastapi import APIRouter, Query, Request, HTTPException
from utils.base import CustomBaseModel, CustomPaginationBaseModel

from utils.base import StateKeywords, AppStateAccessor


class BaseModelViewSet(ABC):
    """ Base class for creating model view sets in FastAPI.
    This class provides a structure for creating base operations for a given model
    """
    model: Type[CustomBaseModel]
    pagination_model: Type[CustomPaginationBaseModel]
    state_key: StateKeywords
    verbose_name: str
    verbose_name_plural: str
    endpoint_prefix: str
    
    
    def __init__(self):
        self.router = APIRouter(prefix=self.endpoint_prefix, tags=[self.verbose_name_plural.capitalize()])
        self.router.add_api_route("/", self.list_view, response_model=self.pagination_model, methods=["GET"], summary=f"List {self.verbose_name_plural.lower()}")
        self.router.add_api_route("/{id_or_uuid}", self.retrieve_view, response_model=self.model, methods=["GET"], summary=f"Retrieve single {self.verbose_name.lower()}")
        self.router.add_api_route("/regenerate", self.regenerate_view, methods=["POST"], summary=f"Regenerate {self.verbose_name_plural.lower()}")
    
    @abstractmethod
    def get_data_with_length(self, request: Request, length: int) -> list:
        pass
    
    @abstractmethod
    def regenerate_func(self, request: Request, length: int) -> None:
        pass
    
    def get_accessor(self, request: Request):
        return AppStateAccessor(request.app.state)
    
    def get_all_data(self, request: Request) -> list:
        return self.get_accessor(request).get(self.state_key)
    
    
    async def list_view(
            self,
            request: Request,
            length: Optional[int] = Query(50, ge=1),
            page: Optional[int] = Query(1, ge=1),
        ):
        length = length if length else 50
        page = page if page else 1
        
        data = self.get_data_with_length(request=request, length=length)
        all_data_length = len(self.get_all_data(request=request)) or 0
        
        if not data:
            raise HTTPException(status_code=503, detail=f"{self.verbose_name_plural.capitalize()} data is not initialized.")
        
        query_params = dict(request.query_params)
        filterable_fields = self.model.get_filterable_fields()
        
        # Apply dynamic filtering based on query parameters
        for field, value in query_params.items():
            if field in filterable_fields:
                data = [item for item in data if str(item.get(field, "")).casefold() == value.casefold()]
        
        # Pagination logic
        start = (page - 1) * length
        end = start + length
        paginated_items = data[start:end]
        
        return self.pagination_model(
            page=page,
            length=length,
            total=all_data_length,
            results=paginated_items,
        )
    
    
    async def retrieve_view(self, id_or_uuid: str, request: Request):
        data = self.get_all_data(request=request)
        if not data:
            raise HTTPException(status_code=503, detail=f"{self.verbose_name_plural.capitalize()} data is not initialized.")
        
        item = next((u for u in data if str(u["id"]) == id_or_uuid or str(u["uuid"]) == id_or_uuid), None)
        if not item:
            raise HTTPException(status_code=404, detail=f"{self.verbose_name.capitalize()} not found")
        return item
    
    
    async def regenerate_view(self, request: Request, length: int = Query(100, ge=1)):
        self.regenerate_func(request=request, length=length)
        return {"message": f"{length} {self.verbose_name_plural.lower()} regenerated."}
