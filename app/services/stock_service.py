from datetime import datetime
from fastapi import UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from models.user import User
from models.stock import Stock
from schemas.requests.stock import StockRequest
from schemas.responses.stock import  StockResponse
from services import image_service
from utils.pagination import create_paginated_response
from utils.query_filter_builder import QueryFilterBuilder

def create_stock(db: Session, user: User, create_stock: StockRequest):
    stock = Stock(**create_stock.model_dump())
    stock.created_by = user.id
    db.add(stock)
    db.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Stock created successfully"})

def get_stock(db: Session, stock_id: str):
    stock = db.query(Stock).filter(Stock.id == stock_id, Stock.is_deleted == False).first()
    if not stock:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Stock not found"})

    stockSchema = StockResponse.model_validate(stock)

    return stockSchema

def get_stocks_query(db: Session, page_no: int, page_size: int, stock_request: StockRequest):
    query_filter = QueryFilterBuilder(Stock).build(stock_request.dict(exclude_unset=True))
    query = db.query(Stock).filter(*query_filter).filter(Stock.is_deleted == False)
    
    # Calculate pagination
    offset = (page_no - 1) * page_size
    paginated_query = query.offset(offset).limit(page_size)
    
    # Get total count and items
    total_count = query.count()
    items = paginated_query.all()
    
    # Create response
    return {
        "items": [StockResponse.model_validate(item) for item in items],
        "total": total_count,
        "page": page_no,
        "size": page_size,
        "pages": (total_count + page_size - 1) // page_size
    }