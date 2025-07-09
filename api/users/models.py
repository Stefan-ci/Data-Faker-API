from pydantic import Field
from typing import Optional
from datetime import datetime
from utils.base import CustomBaseModel, CustomPaginationBaseModel

class UserModel(CustomBaseModel):
    first_name: str
    last_name: str
    email: str
    username: str
    phone_number: str
    birth_date: str
    sex: str
    address: str
    postal_code: str
    city: str
    country: str
    date_joined: datetime
    last_login: datetime
    is_active: bool
    is_staff: bool
    is_superuser: bool
    password: Optional[str]
    
    # excluding "password" on search
    EXCLUDED_FIELDS_ON_SEARCH = {"password"}


class UserPaginationResponse(CustomPaginationBaseModel):
    """ Response model for paginated user list """
    results: list[UserModel] = Field(default_factory=list)
