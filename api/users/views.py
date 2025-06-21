from typing import Optional, List
from fastapi import  Query, Request, APIRouter, HTTPException

from api.users.models import UserModel
from api.users.utils import generate_users_data
from api.base import StateKeywords, AppStateAccessor


class UserApiView:
    def __init__(self):
        self.router = APIRouter(prefix="/users", tags=["Users"])
        self.router.add_api_route("/", self.list_users, response_model=List[UserModel], methods=["GET"], summary="List users")
        self.router.add_api_route("/{user_id}", self.get_user, response_model=UserModel, methods=["GET"], summary="Get single user")
        self.router.add_api_route("/regenerate", self.regenerate_users, methods=["POST"], summary="Regenerate users (overwrite the existing ones)")
    
    
    def get_accessor(self, request: Request):
        return AppStateAccessor(request.app.state)
    
    
    async def list_users(
            self,
            request: Request,
            city: Optional[str] = Query(None),
            length: Optional[int] = Query(50, ge=1)
        ):
        length = length if length else 50
        
        users = self.get_accessor(request).get_or_generate(key=StateKeywords.USERS, func=generate_users_data, length=length)
        
        if city:
            users = [u for u in users if u["city"].casefold() == city.casefold()]
        return users
    
    
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
