import logging
from uuid import UUID
from abc import ABC, abstractmethod
from typing import Type, Optional, Callable, Any, Union
from utils.base import CustomBaseModel, CustomPaginationBaseModel
from utils.base import StateKeywords, AppStateAccessor, Endpoints, Constants
from fastapi import APIRouter, Query, Depends, Request, HTTPException, status


logger = logging.getLogger(__name__)


class BaseModelViewSet(ABC):
    """
    Base class for creating model view sets in FastAPI.
    This class provides a structure for creating base operations for a given model
    """
    model: Type[CustomBaseModel]
    pagination_model: Type[CustomPaginationBaseModel]
    state_key: StateKeywords
    verbose_name: str
    verbose_name_plural: str
    endpoint_data: Endpoints
    tags: Optional[str] = None
    generator_func: Optional[Callable[..., Any]] = None
    
    
    def __init__(self):
        self.router = APIRouter(prefix=self.endpoint_data.endpoint, tags=[self.tags] if self.tags else [self.verbose_name_plural.capitalize()])
        
        # inject filters here and use them in as dependecies
        # that way, parameters (query params) will be defined automatically. No need to define them manually
        self.specific_filter_dependency = self.model._create_filter_dependency_for_model()
        self.router.add_api_route("/regenerate", self.regenerate_view, methods=["POST"], summary=f"Regenerate {self.verbose_name_plural.lower()}")
        self.router.add_api_route(
            "/",
            self.list_view,
            response_model=self.pagination_model,
            methods=["GET"],
            summary=f"List {self.verbose_name_plural.lower()}",
            dependencies=[Depends(self.specific_filter_dependency)], # declaring query params
            name=self.endpoint_data.route_name
        )
        
        self.router.add_api_route(
            "/{id_or_uuid}",
            self.retrieve_view,
            response_model=self.model,
            methods=["GET"],
            summary=f"Retrieve single {self.verbose_name.lower()}",
            name=self.endpoint_data.detail_route_name
        )
    
    
    
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
    
    def get_item_by_id_or_uuid(self, data: list, id_or_uuid: str) -> Optional[dict]:
        return next((item for item in data if str(item.get("id")) == id_or_uuid or str(item.get("uuid")) == id_or_uuid), None)
    
    def validate_id_or_uuid(self, id_or_uuid: str) -> bool:
        """
        FastAPI treats the next string after the provided endpoint as `id_or_uuid`.
        For example: GET http://localhost:9000/users/regenerate will throw back a 404 error on the object.
        To fix it, let's check if the string is a digit or a UUID instance. Else, it should be treated like an endpoint.
        """
        
        # validate ID
        if id_or_uuid.isdigit():
            return True
        
        # validate UUID
        try:
            return id_or_uuid == UUID(id_or_uuid)
        except ValueError as e:
            logger.error(f"Invalid id_or_uuid (ValueError): {e}")
            return False
        except Exception as e:
            logger.error(f"Invalid id_or_uuid: {e}")
            return False
    
    
    async def list_view(self, request: Request, page_size: Optional[int] = Query(Constants.PAGINATE_BY.value, ge=1), page: Optional[int] = Query(1, ge=1),):
        page_size = page_size if page_size else Constants.PAGINATE_BY.value
        page = page if page else 1
        
        filters = self.get_accessor(request).get(StateKeywords._DYNAMIC_FILTERS_DATA)
        data = self.search_data(request=request, length=page_size, filters=filters)
        all_data_length = len(data) or 0
        
        if data is None or not isinstance(data, list):
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"{self.verbose_name_plural.capitalize()} data is not initialized.")
        
        return self.pagination_model(
            page=page,
            page_size=page_size,
            total_obj=all_data_length,
            results=self.paginate_items(page=page, page_size=page_size, data=data),
        )
    
    
    async def retrieve_view(self, id_or_uuid: Union[int, UUID, str], request: Request):
        id_or_uuid_str = str(id_or_uuid)
        
        # validate the provided id_or_uuid
        if not self.validate_id_or_uuid(id_or_uuid=id_or_uuid_str):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"URL not found on this server")
        
        try:
            all_data = self.get_all_data(request=request)
        except AttributeError as e:
            self.regenerate_func(request=request, length=Constants.PAGINATE_BY.value) # regenerate data
            all_data = self.get_all_data(request=request) # re-get data
        except Exception as e:
            logger.error(f"Can't retrieve {self.verbose_name.lower()} data. Error: {e}")
            return None, HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Error while retrieving '{self.verbose_name.capitalize()}': {e}.")
        
        item = self.get_item_by_id_or_uuid(all_data, id_or_uuid_str)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.verbose_name.capitalize()} not found.")
        
        return self.model.model_validate(item) # Validate response with pydantic model
    
    
    async def regenerate_view(self, request: Request, length: int = Query(Constants.PAGINATE_BY.value, ge=1)):
        self.regenerate_func(request=request, length=length)
        return {"message": f"{length} {self.verbose_name_plural.lower()} regenerated."}
