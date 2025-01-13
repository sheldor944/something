from typing import List, TypeVar, Generic
from pydantic import BaseModel

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    current_page_no: int
    total_page_count: int
    page_size: int
    total_item_count: int
    data: List[T]
    has_previous: bool
    has_next: bool