from datetime import datetime
from api.base import CustomBaseModel

class UserModel(CustomBaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: str
    sex: str
    address: str
    postal_code: str
    city: str
    country: str
    date_joined: datetime
