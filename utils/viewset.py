import logging
from uuid import UUID, uuid4
from pydantic import BaseModel
from abc import ABC, abstractmethod
from typing import Type, Optional, Callable, Any, Union
from utils.base import CustomBaseModel, CustomPaginationBaseModel
from utils.base import StateKeywords, AppStateAccessor, Endpoints, Constants
from fastapi import APIRouter, Query, Depends, Request, HTTPException, status, Body


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
        
        # Create input model for POST requests (exclude id and uuid)
        self.create_model = self._create_input_model()
        
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
        
        # Add POST route for creating new items
        self.router.add_api_route(
            "/",
            self.create_view,
            response_model=self.model,
            methods=["POST"],
            summary=f"Create new {self.verbose_name.lower()}",
            name=f"{self.endpoint_data.route_name}_create"
        )
        
        self.router.add_api_route(
            "/{id_or_uuid}/",
            self.retrieve_view,
            response_model=self.model,
            methods=["GET"],
            summary=f"Retrieve single {self.verbose_name.lower()}",
            name=self.endpoint_data.detail_route_name
        )
        
        # Add PUT route for full update
        self.router.add_api_route(
            "/{id_or_uuid}/",
            self.update_view,
            response_model=self.model,
            methods=["PUT"],
            summary=f"Update {self.verbose_name.lower()} (full update)",
            name=f"{self.endpoint_data.detail_route_name}_update"
        )
        
        # Add PATCH route for partial update
        self.router.add_api_route(
            "/{id_or_uuid}/",
            self.partial_update_view,
            response_model=self.model,
            methods=["PATCH"],
            summary=f"Partially update {self.verbose_name.lower()}",
            name=f"{self.endpoint_data.detail_route_name}_partial_update"
        )
    
    
    def _create_input_model(self) -> Type[BaseModel]:
        """
        Create a Pydantic model for input data that excludes 'id' and 'uuid' fields
        """
        model_fields = self.model.model_fields.copy()
        
        # Remove id and uuid from the input model
        model_fields.pop('id', None)
        model_fields.pop('uuid', None)
        
        # Create new model class for input
        from pydantic import create_model
        input_model = create_model(
            f"{self.model.__name__}Create",
            **{name: (field.annotation, field) for name, field in model_fields.items()} # type: ignore
        ) # type: ignore
        
        return input_model
    
    
    def _clean_input_data(self, data: dict) -> dict:
        """
        Remove 'id' and 'uuid' from input data, even if provided by the frontend
        """
        cleaned_data = data.copy()
        cleaned_data.pop('id', None)
        cleaned_data.pop('uuid', None)
        return cleaned_data
    
    
    @abstractmethod
    def get_data_with_length(self, request: Request, length: int) -> list:
        pass
    
    @abstractmethod
    def regenerate_func(self, request: Request, length: int) -> None:
        pass
    
    
    def get_next_id(self, request: Request) -> int:
        """
        Generate the next available ID based on existing data
        """
        try:
            all_data = self.get_all_data(request)
            if not all_data:
                return 1
            
            # Find the maximum ID in existing data
            max_id = max(item.get('id', 0) for item in all_data)
            return max_id + 1
        except:
            return 1
    
    
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
            return str(UUID(id_or_uuid)) == id_or_uuid
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
    
    
    async def create_view(self, request: Request, data: dict = Body(...)):
        """
        Create a new item with auto-generated ID and UUID
        """
        try:
            # Clean input data to remove id and uuid if provided
            cleaned_data = self._clean_input_data(data)
            
            # Get or initialize data in state
            accessor = self.get_accessor(request)
            
            # Ensure the state key exists
            if not accessor.exists(self.state_key):
                accessor.set(self.state_key, [])
            
            # Get current data
            current_data = accessor.get(self.state_key)
            
            # Generate new ID and UUID
            new_id = self.get_next_id(request)
            new_uuid = str(uuid4())
            
            # Create the new item with generated ID and UUID
            new_item = {
                "id": new_id,
                "uuid": new_uuid,
                **cleaned_data  # Add all the cleaned fields from the request body
            }
            
            # Validate the new item with the model
            validated_item = self.model.model_validate(new_item)
            
            # Add to the data list
            current_data.append(validated_item.model_dump())
            
            # Update state
            accessor.set(self.state_key, current_data)
            
            logger.info(f"Created new {self.verbose_name.lower()} with ID: {new_id} and UUID: {new_uuid}")
            
            return validated_item
            
        except Exception as e:
            logger.error(f"Error creating {self.verbose_name.lower()}: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Error creating {self.verbose_name.lower()}: {str(e)}"
            )
    
    
    async def update_view(self, id_or_uuid: Union[int, UUID, str], request: Request, data: dict = Body(...)):
        """
        Full update (PUT) - replaces all fields except id and uuid
        """
        try:
            id_or_uuid_str = str(id_or_uuid)
            
            # Validate the provided id_or_uuid
            if not self.validate_id_or_uuid(id_or_uuid=id_or_uuid_str):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"URL not found on this server")
            
            # Clean input data to remove id and uuid if provided
            cleaned_data = self._clean_input_data(data)
            
            # Get current data
            accessor = self.get_accessor(request)
            current_data = accessor.get(self.state_key)
            
            if not current_data:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.verbose_name.capitalize()} not found.")
            
            # Find the item to update
            item_index = None
            original_item = {}
            
            for i, item in enumerate(current_data):
                if str(item.get("id")) == id_or_uuid_str or str(item.get("uuid")) == id_or_uuid_str:
                    item_index = i
                    original_item = item
                    break
            
            if item_index is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.verbose_name.capitalize()} not found.")
            
            # Create updated item (keep original id and uuid)
            updated_item = {
                "id": original_item["id"],
                "uuid": original_item["uuid"],
                **cleaned_data  # Replace all other fields
            }
            
            # Validate the updated item
            validated_item = self.model.model_validate(updated_item)
            
            # Update in the data list
            current_data[item_index] = validated_item.model_dump()
            
            # Update state
            accessor.set(self.state_key, current_data)
            
            logger.info(f"Updated {self.verbose_name.lower()} with ID/UUID: {id_or_uuid_str}")
            
            return validated_item
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating {self.verbose_name.lower()}: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Error updating {self.verbose_name.lower()}: {str(e)}"
            )
    
    
    async def partial_update_view(self, id_or_uuid: Union[int, UUID, str], request: Request, data: dict = Body(...)):
        """
        Partial update (PATCH) - updates only provided fields, keeps others unchanged
        """
        try:
            id_or_uuid_str = str(id_or_uuid)
            
            # Validate the provided id_or_uuid
            if not self.validate_id_or_uuid(id_or_uuid=id_or_uuid_str):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"URL not found on this server")
            
            # Clean input data to remove id and uuid if provided
            cleaned_data = self._clean_input_data(data)
            
            # Get current data
            accessor = self.get_accessor(request)
            current_data = accessor.get(self.state_key)
            
            if not current_data:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.verbose_name.capitalize()} not found.")
            
            # Find the item to update
            item_index = None
            original_item = {}
            
            for i, item in enumerate(current_data):
                if str(item.get("id")) == id_or_uuid_str or str(item.get("uuid")) == id_or_uuid_str:
                    item_index = i
                    original_item = item.copy()
                    break
            
            if item_index is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.verbose_name.capitalize()} not found.")
            
            # Update only the provided fields (keep original id, uuid, and non-provided fields)
            updated_item = original_item.copy()
            updated_item.update(cleaned_data)  # Only update provided fields
            
            # Validate the updated item
            validated_item = self.model.model_validate(updated_item)
            
            # Update in the data list
            current_data[item_index] = validated_item.model_dump()
            
            # Update state
            accessor.set(self.state_key, current_data)
            
            logger.info(f"Partially updated {self.verbose_name.lower()} with ID/UUID: {id_or_uuid_str}")
            
            return validated_item
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error partially updating {self.verbose_name.lower()}: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Error partially updating {self.verbose_name.lower()}: {str(e)}"
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
