from enum import Enum
from uuid import UUID
from faker import Faker
from typing import Callable
from pydantic import BaseModel
from abc import ABC, abstractmethod


class BaseDataGenerator(ABC):
    def __init__(self, locale="en_US"):
        self.locale = locale
        # multi-locale doesn't support all methods for now, so use it wisely or simply deactivate it
        self.fake = Faker(locale=self.locale)
    
    @abstractmethod
    def generate(self, n):
        pass


class StateKeywords(Enum):
    """ Utility used to store data in state based centralized keywords """
    USERS = ("users", "Keyword to store users list in the state")
    EMPLOYEES = ("employees", "Keyword to store employees list in the state")
    MEDICAL = ("medical", "Keyword to medical data of patients in the state")
    PRODUCTS = ("products", "Keyword to store products list in the state")
    ORDERS = ("orders", "Keyword to store orders list in the state")
    LOCALE_LANG = ("locale", "Keyword to store the default language in the state")
    
    def __init__(self, key: str, description: str):
        self._key = key
        self.description = description
    
    @property
    def key(self) -> str:
        return self._key
    
    def __str__(self) -> str:
        return self._key


class AppStateAccessor:
    def __init__(self, state):
        self._state = state
    
    def get(self, key: StateKeywords):
        return getattr(self._state, key.key)
    
    def set(self, key: StateKeywords, value):
        setattr(self._state, key.key, value)
    
    def exists(self, key: StateKeywords) -> bool:
        return hasattr(self._state, key.key)
    
    def get_or_generate(self, key: StateKeywords, func: Callable[..., list], *, length=50, **kwargs):
        """
        Returns the value from state if exists, otherwise generates it using `func`.
        The generated data is stored in the state.
        
        Args:
            key (StateKeywords): Key used to store/get data from the state.
            func (Callable[..., list]): Function to generate data if they don't exists.
            length (int, optional): How many items should be generated. Defaults to 50.
        """
        if not self.exists(key):
            self.set(key, func(length=length, **kwargs))
        return self.get(key)


class CustomBaseModel(BaseModel):
    id: int
    uuid: UUID


class SexChoices(Enum):
    MALE = "male"
    FEMALE = "female"


class AllergiesChoices(Enum):
    Peanuts = "Peanuts"
    Dust = "Dust"
    Latex = "Latex"
    _None = "None"
    Shellfish = "Shellfish"


class DepartmentChoices(Enum):
    HR = "HR"
    Finance = "Finance"
    IT = "IT"
    Sales = "Sales"
    Marketing = "Marketing"
    CustomerService = "Customer Service"
    Legal = "Legal"
    Operations = "Operations"
    RnD = "R&D"
    Procurement = "Procurement"
    Administration = "Administration"
    Logistics = "Logistics"
    QualityAssurance = "Quality Assurance"


class ProductCategories(Enum):
    Electronics = "Electronics"
    Home = "Home"
    Fashion = "Fashion"
    Beauty = "Beauty"
    Food = "Food"
    Sports = "Sports"
    Toys = "Toys"
    Automotive = "Automotive"
    Books = "Books"
    Health = "Health"
    Garden = "Garden"
    Office = "Office"
    Jewelry = "Jewelry"
    Music = "Music"
    Pets = "Pets"
    Tools = "Tools"
    Baby = "Baby"
    Outdoors = "Outdoors"
