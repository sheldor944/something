from sqlalchemy.orm import Query
from sqlalchemy.ext.declarative import DeclarativeMeta
from typing import Type, TypeVar, Optional, List

T = TypeVar('T', bound=DeclarativeMeta)

class QueryFilterBuilder:
    def __init__(self, model: Type[T]):
        self.model = model
        self.filters: List = []

    def exact_filter(self, attribute_name: str, value: Optional[str]):
        if not value:
            return self
        attr = getattr(self.model, attribute_name, None)
        if attr is not None:
            self.filters.append(attr == value)
        return self
    
    def prefix_filter(self, attribute_name: str, value: Optional[str]):
        if not value:
            return self
        attr = getattr(self.model, attribute_name, None)
        if attr is not None:
            self.filters.append(attr.startswith(value))
        return self
    
    def suffix_filter(self, attribute_name: str, value: Optional[str]):
        if not value:
            return self
        attr = getattr(self.model, attribute_name, None)
        if attr is not None:
            self.filters.append(attr.endswith(value))
        return self
    
    def contains_filter(self, attribute_name: str, value: Optional[str]):
        if not value:
            return self
        attr = getattr(self.model, attribute_name, None)
        if attr is not None:
            self.filters.append(attr.contains(value))
        return self
    
    def build(self, filter_dict: dict):
        for key, value in filter_dict.items():
            if value:
                self.exact_filter(key, value)
        return self.filters