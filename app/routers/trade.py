from fastapi import APIRouter, File, UploadFile, Query, Depends
from schemas.requests.trade import TradeCloseRequest, TradeCreateRequest, TradeFilter, TradeCreateRequestAutomated, TradeCloseRequestAutomated
from services import trade_service
from dependency import get_db_session, get_current_user

router = APIRouter(
    tags=["trade"]
)

@router.post("/trade")
def create_trade(db: get_db_session, user: get_current_user, create_trade: TradeCreateRequest):
    return trade_service.create_trade(db, user, create_trade)

@router.put("/trade/close")
def close_trade(db: get_db_session, user: get_current_user, close_trade: TradeCloseRequest):
    return trade_service.close_trade(db, user, close_trade)

@router.get("/trade/{trade_id}")
def get_trade(db: get_db_session, trade_id: str ):
    return trade_service.get_trade(db, trade_id)

@router.get("/trades")
def get_all_by_filter(db: get_db_session, user_id: str, trade_request_filter : TradeFilter = Depends(None)):
    return trade_service.get_all_by_filter(db, user_id, trade_request_filter)

@router.post("/trade/automated")
def create_trade_automated(db: get_db_session, create_trade: TradeCreateRequestAutomated):
    print("create_trade_automated in the router ", create_trade)
    return trade_service.create_trade_automatic(db, create_trade)

@router.put("/trade_close/automated")
def close_trade_automated(db: get_db_session, close_trade: TradeCloseRequestAutomated):
    return trade_service.close_trade_automatic(db, close_trade)