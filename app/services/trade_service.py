from datetime import datetime, date
from fastapi import UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from models.user import User
from models.trade import Trade
from schemas.requests.trade import TradeCreateRequest, TradeCloseRequest, TradeFilter
from schemas.responses.trade import  TradeResponse
from models.account import Account, Transaction, AutomatedAccount
from utils.query_filter_builder import QueryFilterBuilder
from schemas.requests.accounts import TransactionRequest
from models.stock import Stock


def create_trade(db: Session, user: User, create_trade: TradeCreateRequest):

    account = db.query(Account).filter(Account.user_id == user.id, Account.is_deleted == False).first()
    
    if not account:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Account not found"})
    automated_account = db.query(AutomatedAccount).filter(AutomatedAccount.account_id == account.id, AutomatedAccount.is_deleted == False).first()
    if account.balance < create_trade.trade_start_price * create_trade.quantity and create_trade.is_Automated == False:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Insufficient balance"})
    if create_trade.is_Automated == True and account.automated_balance < create_trade.trade_start_price * create_trade.quantity:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Insufficient automated balance"})
    if create_trade.is_Automated == False:
        account.balance = account.balance - create_trade.trade_start_price * create_trade.quantity
    if create_trade.is_Automated == True:
        if not automated_account:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Automated Account not found"})
        automated_account.balance = automated_account.balance - create_trade.trade_start_price * create_trade.quantity
        account.automated_balance = account.automated_balance - create_trade.trade_start_price * create_trade.quantity
    stock = db.query(Stock).filter(Stock.id == create_trade.stock_id, Stock.is_deleted == False).first()
    print("stock is ", stock)
    transaction_request = TransactionRequest(
        # account_id = account.id,
        transaction_type = "DEBIT",
        symbol = stock.symbol,
        amount=create_trade.trade_start_price * create_trade.quantity,
        transaction_status = "COMPLETED",
        transaction_date = datetime.now(),
        transaction_done_by = create_trade.is_Automated and "AUTOMATED" or "MANUAL"
    )
    transaction = Transaction(**transaction_request.model_dump())
    transaction.account_id = account.id
    transaction.created_by = user.id
    db.add(transaction)
    trade = Trade(**create_trade.model_dump())
    trade.user_id = user.id
    trade.created_by = user.id
    trade.trade_status = "OPEN"
    db.add(trade)
    db.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Trade created successfully"})

def close_trade(db: Session, user: User, close_trade: TradeCloseRequest):
    account = db.query(Account).filter(Account.user_id == user.id, Account.is_deleted == False).first()
    if not account:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Account not found"})
    
    automated_account = db.query(AutomatedAccount).filter(AutomatedAccount.account_id == account.id, AutomatedAccount.is_deleted == False).first()
    trade_id = close_trade.trade_id
    trade = db.query(Trade).filter(Trade.id == trade_id, Trade.is_deleted == False).first()
    if not trade:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Trade not found"})
        
    trade.trade_end_price = close_trade.trade_end_price
    trade.trade_end_date = close_trade.trade_end_date
    trade.trade_status = "CLOSED"
    profit = (trade.trade_end_price - trade.trade_start_price) * trade.quantity * (trade.trade_type == "LONG" and 1 or -1)
    selling_price = trade.trade_end_price * trade.quantity
    trade.trade_profit = profit
    trade.updated_by = user.id
    profit = profit + selling_price
    if trade.is_Automated == False:
        account.balance = account.balance + profit
    if trade.is_Automated == True:
        automated_account.balance = automated_account.balance + profit
        account.automated_balance = account.automated_balance + profit
    stock = trade.stock
    transaction_request = TransactionRequest(
        transaction_type = "CREDIT",
        symbol = stock.symbol,
        amount = profit,
        transaction_status = "COMPLETED",
        transaction_date = datetime.now(),
        transaction_done_by = trade.is_Automated and "AUTOMATED" or "MANUAL"
    )
    transaction = Transaction(**transaction_request.model_dump())
    transaction.account_id = account.id
    transaction.created_by = user.id
    db.add(transaction)
    
    # if profit > 0:
    #     if trade.is_Automated == False:
    #         account.balance = account.balance + profit
        
    #     stock = trade.stock
    #     transaction_request = TransactionRequest(
    #         account_id = account.id,
    #         transaction_type = "CREDIT",
    #         symbol = stock.symbol,
    #         amount = profit,
    #         transaction_status = "COMPLETED",
    #         transaction_date = date.today()
    #     )
    #     transaction = Transaction(**transaction_request.model_dump())
    #     transaction.created_by = user.id
    #     db.add(transaction)
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
