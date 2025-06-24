from enum import Enum
from uuid import UUID
from faker import Faker
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import Callable, ClassVar, Set, TypeVar, Generic, List

T = TypeVar("T")

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
    USERS = ("users", "Keyword to store users in the state")
    EMPLOYEES = ("employees", "Keyword to store employees in the state")
    MEDICAL = ("medical", "Keyword to medical data of patients in the state")
    PRODUCTS = ("products", "Keyword to store products in the state")
    ORDERS = ("orders", "Keyword to store orders in the state")
    INCOMES = ("incomes", "Keyword to store incomes in the state")
    EXPENSES = ("expenses", "Keyword to store expenses in the state")
    PAYMENTS = ("payments", "Keyword to store payments in the state")
    NOTIFICATIONS = ("notifications", "Keyword to store notifications in the state")
    ATTENDANCES = ("attendances", "Keyword to store attendances in the state")
    TODOS = ("todos", "Keyword to store todos in the state")
    CHATS = ("chats", "Keyword to store chats in the state")
    ANALYTICS = ("analytics", "Keyword to store analytics in the state")
    CRYPTOS = ("cryptos", "Keyword to store cryptos in the state")
    
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
            self.set(key=key, value=func(length=length, **kwargs))
        return self.get(key)


class CustomBaseModel(BaseModel):
    id: int
    uuid: UUID
    
    # used to exclude fields from search
    EXCLUDED_FIELDS_ON_SEARCH: ClassVar[Set[str]] = set()
    
    @classmethod
    def get_filterable_fields(cls) -> set[str]:
        return {
            name for name in cls.model_fields.keys()
            if name not in cls.EXCLUDED_FIELDS_ON_SEARCH
        }


class CustomPaginationBaseModel(BaseModel, Generic[T]):
    page: int
    length: int
    total: int
    results: List[T] = Field(default_factory=list)


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
