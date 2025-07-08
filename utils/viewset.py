from abc import ABC, abstractmethod
from typing import Type, Optional, Callable, Any
from utils.base import StateKeywords, AppStateAccessor
from utils.base import CustomBaseModel, CustomPaginationBaseModel
from fastapi import APIRouter, Query, Depends, Request, HTTPException


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
    tags: Optional[str] = None
    generator_func: Optional[Callable[..., Any]] = None
    
    
    def __init__(self):
        self.router = APIRouter(prefix=self.endpoint_prefix, tags=[self.tags] if self.tags else [self.verbose_name_plural.capitalize()])
        
        # inject filters here and use them in as dependecies
        # that way, parameters (query params) will be defined automatically. No need to define them manually
        self.specific_filter_dependency = self.model._create_filter_dependency_for_model()
        self.router.add_api_route(
            "/",
            self.list_view,
            response_model=self.pagination_model,
            methods=["GET"],
            summary=f"List {self.verbose_name_plural.lower()}",
            dependencies=[Depends(self.specific_filter_dependency)] # declaring query params
        )
        
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
    
    def get_all_data(self, request: Request):
        return self.get_accessor(request).get(self.state_key)
    
    
    
    def search_data(self, request: Request, length: int, filters: Optional[dict] = None) -> list:
        data = self.get_data_with_length(request=request, length=length)
        
        if not filters:
            return data
        
        
        for field, value in filters.items():
            filtered_data = []
            for item in data:
                item_value = item.get(field)
                
                # Case 1: filter's value is None
                if value is None:
                    if item_value is None:
                        filtered_data.append(item)
                
                # Case 2: filter's value is not None
                elif item_value is not None:
                    # search by "icontains" if both are str
                    if isinstance(item_value, str) and isinstance(value, str):
                        if value.casefold() in item_value.casefold():
                            filtered_data.append(item)
                    # Sinon (types numériques, dates, UUID, etc.), applique une égalité exacte
                    elif item_value == value:
                        filtered_data.append(item)
            
            data = filtered_data # update "data" for the next filter
        
        return data
    
    def paginate_items(self, page: int, page_size: int, data: list):
        start = (page - 1) * page_size
        end = start + page_size
        return data[start:end]
    
    
    
    async def list_view(self, request: Request, page_size: Optional[int] = Query(50, ge=1), page: Optional[int] = Query(1, ge=1),):
        page_size = page_size if page_size else 50
        page = page if page else 1
        
        filters = self.get_accessor(request).get(StateKeywords._DYNAMIC_FILTERS_DATA)
        data = self.search_data(request=request, length=page_size, filters=filters)
        all_data_length = len(data) or 0
        
        if data is None or not isinstance(data, list):
            raise HTTPException(status_code=503, detail=f"{self.verbose_name_plural.capitalize()} data is not initialized.")
        
        return self.pagination_model(
            page=page,
            page_size=page_size,
            total_obj=all_data_length,
            results=self.paginate_items(page=page, page_size=page_size, data=data),
        )
    
    
    async def retrieve_view(self, id_or_uuid: str, request: Request):
        try:
            data = self.get_all_data(request=request)
        except AttributeError as e:
            self.regenerate_func(request=request, length=50) # regenerate data
            data = self.get_all_data(request=request) # re-get data
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Error while retrieving '{self.verbose_name.capitalize()}': {e}.")
        
        if not data:
            raise HTTPException(status_code=503, detail=f"{self.verbose_name_plural.capitalize()} data is not initialized.")
        
        item = next((u for u in data if str(u["id"]) == id_or_uuid or str(u["uuid"]) == id_or_uuid), None)
        if not item:
            raise HTTPException(status_code=404, detail=f"{self.verbose_name.capitalize()} not found")
        return item
    
    
    async def regenerate_view(self, request: Request, length: int = Query(100, ge=1)):
        self.regenerate_func(request=request, length=length)
        return {"message": f"{length} {self.verbose_name_plural.lower()} regenerated."}
