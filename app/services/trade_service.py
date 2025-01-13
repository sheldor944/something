from datetime import datetime
from fastapi import UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from models.user import User
from models.trade import Trade
from schemas.requests.trade import TradeCreateRequest, TradeCloseRequest, TradeFilter
from schemas.responses.trade import  TradeResponse

from utils.query_filter_builder import QueryFilterBuilder


def create_trade(db: Session, user: User, create_trade: TradeCreateRequest):
    trade = Trade(**create_trade.model_dump())
    trade.user_id = user.id
    trade.created_by = user.id
    trade.trade_status = "OPEN"
    db.add(trade)
    db.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Trade created successfully"})

def close_trade(db: Session, user: User, close_trade: TradeCloseRequest):
    trade_id = close_trade.trade_id
    trade = db.query(Trade).filter(Trade.id == trade_id, Trade.is_deleted == False).first()
    if not trade:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Trade not found"})

    trade.trade_end_price = close_trade.trade_end_price
    trade.trade_end_date = close_trade.trade_end_date
    trade.trade_status = "CLOSED"
    profit = (trade.trade_end_price - trade.trade_start_price) * trade.quantity * (trade.trade_type == "LONG" and 1 or -1)
    trade.trade_profit = profit
    trade.updated_by = user.id
    db.commit()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Trade closed successfully"})

def get_trade(db: Session, trade_id: str):
    trade = db.query(Trade).filter(Trade.id == trade_id, Trade.is_deleted == False).first()
    if not trade:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Trade not found"})

    tradeSchema = TradeResponse.model_validate(trade)

    return tradeSchema

def get_all_by_filter(db: Session, user_id: str, trade_request_filter : TradeFilter ):
    query = db.query(Trade).filter(Trade.user_id == user_id, Trade.is_deleted == False)
    if trade_request_filter:
        if trade_request_filter.trade_id:
            query = query.filter(Trade.id == trade_request_filter.trade_id)
        if trade_request_filter.stock_id:
            query = query.filter(Trade.stock_id == trade_request_filter.stock_id)
        if trade_request_filter.symbol:
            query = query.join(Trade.stock).filter(Trade.stock.symbol == trade_request_filter.symbol)
        if trade_request_filter.trade_start_date:
            query = query.filter(Trade.trade_start_date >= trade_request_filter.trade_start_date)
        if trade_request_filter.trade_end_date:
            query = query.filter(Trade.trade_end_date <= trade_request_filter.trade_end_date)
        if trade_request_filter.trade_type:
            query = query.filter(Trade.trade_type == trade_request_filter.trade_type)
        if trade_request_filter.trade_status:
            query = query.filter(Trade.trade_status == trade_request_filter.trade_status)
    
    trades = query.order_by(desc(Trade.trade_end_date)).all()
    trades = db.query(Trade).filter(Trade.created_by == user_id, Trade.is_deleted == False).all()
    return [TradeResponse.model_validate(trade) for trade in trades]
