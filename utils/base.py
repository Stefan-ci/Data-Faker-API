from enum import Enum
from uuid import UUID
from faker import Faker
from abc import ABC, abstractmethod
from fastapi import Query, Depends, Request
from pydantic import BaseModel, Field, create_model
from typing import Callable, ClassVar, Set, TypeVar, Generic, List, Optional

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
    ORDER_ITEMS = ("order-items", "Keyword to store order items in the state")
    INCOMES = ("incomes", "Keyword to store incomes in the state")
    EXPENSES = ("expenses", "Keyword to store expenses in the state")
    PAYMENTS = ("payments", "Keyword to store payments in the state")
    NOTIFICATIONS = ("notifications", "Keyword to store notifications in the state")
    ATTENDANCES = ("attendances", "Keyword to store attendances in the state")
    TODOS = ("todos", "Keyword to store todos in the state")
    CHATS = ("chats", "Keyword to store chats in the state")
    ANALYTICS = ("analytics", "Keyword to store analytics in the state")
    CRYPTOS = ("cryptos", "Keyword to store cryptos in the state")
    CRYPTO_TRANSACTIONS = ("crypto_transactions", "Keyword to store crypto transactions in the state")
    FEEDBACKS = ("feedbacks", "Keyword to store feedbacks in the state")
    
    
    _DYNAMIC_FILTERS_DATA = ("_dynamic_filters_data", "Keyword to store dynamic filters data in the state")
    
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
    
    def get(self, key: StateKeywords|str):
        if isinstance(key, str):
            return getattr(self._state, key)
        return getattr(self._state, key.key)
    
    def set(self, key: StateKeywords, value):
        setattr(self._state, key.key, value)
        return self.get(key=key)
    
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



class Endpoints(Enum):
    ANALYTICS_BASE_ENDPOINT = ("/analytics", "Fake analytics data", "analytics-list")
    ATTENDANCES_BASE_ENDPOINT = ("/attendances", "Fake attendances data", "attendances-list")
    CHATS_BASE_ENDPOINT = ("/chats", "Fake chats data", "chats-list")
    CRYPTOS_BASE_ENDPOINT = ("/cryptos", "Fake cryptos data", "cryptos-list")
    CRYPTOS_TRANSACTIONS_BASE_ENDPOINT = ("/cryptos-transactions", "Fake cryptos transactions data", "cryptos_transactions-list")
    EMPLOYEES_BASE_ENDPOINT = ("/employees", "Fake employees data", "employees-list")
    EXPENSES_BASE_ENDPOINT = ("/expenses", "Fake expenses data", "expenses-list")
    INCOMES_BASE_ENDPOINT = ("/incomes", "Fake incomes data", "incomes-list")
    MEDICAL_DATA_BASE_ENDPOINT = ("/medical", "Fake medical data", "medical-list")
    NOTIFICATIONS_BASE_ENDPOINT = ("/notifications", "Fake notifications data", "notifications-list")
    ORDERS_BASE_ENDPOINT = ("/orders", "Fake orders data", "orders-list")
    ORDER_ITEMS_BASE_ENDPOINT = ("/order-items", "Fake order items data", "order_items-list")
    PAYMENTS_BASE_ENDPOINT = ("/payments", "Fake payments data", "payments-list")
    PRODUCTS_BASE_ENDPOINT = ("/products", "Fake products data", "products-list")
    TODOS_BASE_ENDPOINT = ("/todos", "Fake todos data", "todos-list")
    USERS_BASE_ENDPOINT = ("/users", "Fake users data", "users-list")
    FEEDBACKS_BASE_ENDPOINT = ("/feedbacks", "Fake feedbacks data", "feedbacks-list")
    
    def __init__(self, endpoint_prefix: str, description: str, route_name: str):
        self._endpoint_prefix = endpoint_prefix
        self.description = description
        self._route_name = route_name
    
    
    @property
    def endpoint(self) -> str:
        return self._endpoint_prefix
    
    @property
    def route_name(self) -> str:
        return self._route_name
    
    @property
    def detail_route_name(self) -> str:
        return f"retrieve_single_{self.endpoint.lower()}"
    
    @property
    def list_route_name(self) -> str:
        return self.route_name
    
    def __str__(self) -> str:
        return self.description



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
    
    
    @classmethod
    def _create_filter_dependency_for_model(cls) -> Callable[[Request], None]:
        filterable_fields = cls.get_filterable_fields()
        pydantic_fields = {}
        
        for field_name in filterable_fields:
            model_field = cls.model_fields.get(field_name)
            if model_field:
                field_type = Optional[model_field.annotation]
                pydantic_fields[field_name] = (field_type, Query(None, description=f"Filter by {field_name}"))
            else:
                pydantic_fields[field_name] = (Optional[str], Query(None, description=f"Filter by {field_name}"))
        
        FilterModel = create_model(f"{cls.__name__}Filter", **pydantic_fields)
        
        def _actual_filter_injector(request: Request, filters_params: FilterModel = Depends()) -> None: # type: ignore
            AppStateAccessor(request.app.state).set(key=StateKeywords._DYNAMIC_FILTERS_DATA, value=filters_params.model_dump(exclude_none=True))
        
        return _actual_filter_injector


class CustomPaginationBaseModel(BaseModel, Generic[T]):
    page: int
    page_size: int
    total_obj: int
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
