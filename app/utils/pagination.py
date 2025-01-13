from typing import Type, TypeVar
from sqlalchemy.orm import Query
from pydantic import BaseModel
from schemas.responses.pagination import PaginatedResponse  

T = TypeVar('T', bound=BaseModel)

def create_paginated_response(query: Query, page_no: int, page_size: int, schema_class: Type[T]) -> PaginatedResponse[T]:
    total_item_count = query.count()
    total_page_count = (total_item_count + page_size - 1) // page_size  
    
    items = query.offset((page_no - 1) * page_size).limit(page_size).all()
    item_schemas = [schema_class.model_validate(item) for item in items]  

    return PaginatedResponse[T](
        current_page_no=page_no,
        total_page_count=total_page_count,
        page_size=page_size,
        total_item_count=total_item_count,
        data=item_schemas,
        has_previous=page_no > 1,
        has_next=page_no < total_page_count
    )