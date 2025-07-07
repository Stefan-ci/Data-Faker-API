import operator
from typing import Any, Callable, Generic, TypeVar, Type

T = TypeVar("T")

LOOKUP_OPERATORS: dict[str, Callable[[Any, Any], bool]] = {
    "exact": operator.eq,
    "lt": operator.lt,
    "lte": operator.le,
    "gt": operator.gt,
    "gte": operator.ge,
    "icontains": lambda a, b: b.lower() in a.lower() if isinstance(a, str) else False,
    "in": lambda a, b: a in b,
}


def parse_lookup(key: str) -> tuple[str, str]:
    if "__" in key:
        field, lookup = key.split("__", 1)
    else:
        field, lookup = key, "exact"
    return field, lookup


class BaseQuerySet(Generic[T]):
    """ Query set to be used on models """
    def __init__(self, model: Type[T], data: list[T]):
        self.model = model
        self._data = data
    
    def _match(self, obj: T, **kwargs) -> bool:
        for key, value in kwargs.items():
            field, lookup = parse_lookup(key)
            op = LOOKUP_OPERATORS.get(lookup)
            if not op:
                raise ValueError(f"Unsupported lookup: {lookup}")
            attr = getattr(obj, field, None)
            if not op(attr, value):
                return False
        return True
    
    def filter(self, **kwargs):
        # simple case-insensitive filtering
        def matches(obj):
            return all(str(getattr(obj, k, "")).casefold() == str(v).casefold() for k, v in kwargs.items())
        return BaseQuerySet(self.model, [obj for obj in self._data if matches(obj)])
    
    def get_or_none(self, **kwargs):
        try:
            return self.filter(**kwargs).first()
        except Exception:
            return None
    
    def exclude(self, **kwargs) -> "BaseQuerySet[T]":
        filtered = [obj for obj in self._data if not self._match(obj, **kwargs)]
        return BaseQuerySet(self.model, filtered)
    
    def get(self, **kwargs) -> T:
        matches = self.filter(**kwargs)._data
        if not matches:
            raise ValueError(f"No {self.model.__name__} found for {kwargs}")
        if len(matches) > 1:
            raise ValueError(f"Multiple {self.model.__name__} instances found for {kwargs}")
        return matches[0]
    
    def only(self, *fields: str) -> list[dict[str, Any]]:
        return [
            {field: getattr(obj, field) for field in fields if hasattr(obj, field)}
            for obj in self._data
        ]
    
    def values(self, *fields: str) -> list[dict[str, Any]]:
        return self.only(*fields)
    
    def values_list(self, *fields: str, flat=False) -> list[Any]:
        if flat:
            if len(fields) != 1:
                raise ValueError("flat=True requires exactly one field.")
            return [getattr(obj, fields[0]) for obj in self._data]
        return [tuple(getattr(obj, f) for f in fields) for obj in self._data]
    
    def order_by(self, *fields: str) -> "BaseQuerySet[T]":
        def get_sort_key(obj: T):
            key = []
            for f in fields:
                reverse = f.startswith("-")
                field = f.lstrip("-")
                val = getattr(obj, field, None)
                key.append((not reverse, val))  # sort ascending by default
            return key
        
        sorted_data = sorted(self._data, key=get_sort_key)
        return BaseQuerySet(self.model, sorted_data)
    
    def all(self) -> list[T]:
        return self._data
    
    def count(self) -> int:
        return len(self._data)
    
    def first(self) -> T | None:
        return self._data[0] if self._data else None
    
    def last(self) -> T | None:
        return self._data[-1] if self._data else None
    
    def paginate(self, page: int, length: int):
        start = (page - 1) * length
        return self._data[start:start + length]
    
    def exists(self):
        return bool(self._data)
