from typing import Optional
from fastapi import  Query, Request, APIRouter, HTTPException

from api.users.utils import generate_users_data
from utils.base import StateKeywords, AppStateAccessor
from api.users.models import UserModel, UserPaginationResponse


class UserApiView:
    def __init__(self):
        self.router = APIRouter(prefix="/users", tags=["Users"])
        self.router.add_api_route("/", self.list_users, response_model=UserPaginationResponse, methods=["GET"], summary="List users")
        self.router.add_api_route("/{user_id}", self.get_user, response_model=UserModel, methods=["GET"], summary="Get single user")
        self.router.add_api_route("/regenerate", self.regenerate_users, methods=["POST"], summary="Regenerate users (overwrite the existing ones)")
    
    
    def get_accessor(self, request: Request):
        return AppStateAccessor(request.app.state)
    
    
    async def list_users(
            self,
            request: Request,
            length: Optional[int] = Query(50, ge=1),
            page: Optional[int] = Query(1, ge=1)
        ):
        length = length if length else 50
        page = page if page else 1
        users = self.get_accessor(request).get_or_generate(key=StateKeywords.USERS, func=generate_users_data, length=length)
        all_users_length = len(self.get_accessor(request).get(StateKeywords.USERS)) or 0
        
        if not users:
            raise HTTPException(status_code=503, detail="Users data is not initialized.")
        
        query_params = dict(request.query_params)
        filterable_fields = UserModel.get_filterable_fields()
        
        # Dynamic filtering based on query parameters
        for field, value in query_params.items():
            if field in filterable_fields:
                users = [u for u in users if str(u.get(field, "")).casefold() == value.casefold()]
        
        # Pagination logic
        start = (page - 1) * length
        end = start + length
        users = users[start:end]
        
        return UserPaginationResponse(
            page=page,
            length=length,
            total=all_users_length,
            results=users,
        )
    
    
    async def get_user(self, user_id: str, request: Request):
        users = self.get_accessor(request).get_or_generate(key=StateKeywords.USERS, func=generate_users_data)
        
        if not users:
            raise HTTPException(status_code=503, detail="Users data is not initialized.")
        
        user = next((u for u in users if str(u["id"]) == user_id or str(u["uuid"]) == user_id), None)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    
    async def regenerate_users(self, request: Request, length: int = Query(100, ge=1)):
        self.get_accessor(request).set(key=StateKeywords.USERS, value=generate_users_data(length=length))
        return {"message": f"{length} users regenerated."}
