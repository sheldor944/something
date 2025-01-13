from fastapi import APIRouter, File, UploadFile, Query, Depends
from schemas.requests.stock import StockRequest
from services import stock_service
from dependency import get_db_session, get_current_user

router = APIRouter(
    tags=["stock"]
)

@router.post("/stock")
def create_stock(db: get_db_session, user: get_current_user, create_stock: StockRequest):
    return stock_service.create_stock(db, user, create_stock)

@router.get("/stock/{stock_id}")
def get_stock(db: get_db_session, stock_id: str ):
    return stock_service.get_stock(db, stock_id)

@router.get("/stocksQuery")
def get_stocks_query(db: get_db_session,
                    page_no: int = Query(1, ge=1, description="Page number"), 
                    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
                    stock_request : StockRequest = Depends()):
    return stock_service.get_stocks_query(db, page_no, page_size, stock_request)