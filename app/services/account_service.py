from datetime import datetime
from fastapi import UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from models.user import User
from models.trade import Trade
from schemas.requests.accounts import AccountRequest, AccountUpdateRequest
from schemas.responses.account import  AccountResponse
from models.account import Account
from models.account import Transaction


def create_account(db: Session, user: User, account_request: AccountRequest):
    account = Account(**account_request.model_dump())
    account.created_by = user.id
    db.add(account)
    db.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Account created successfully"})

def update_account(db: Session, user_id: str, account_update_request: AccountUpdateRequest):
    account = db.query(Account).filter(Account.user_id == user_id, Account.is_deleted == False).first()
    if not account:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Account not found"})
    if account_update_request.amount is not None:
        print("account.balance before update ", account.balance)
        if account_update_request.modificationType == True:
            account.balance = account.balance + account_update_request.amount
        else:
            account.balance = account.balance - account_update_request.amount

   
    db.commit()
    accountSchema = AccountResponse.model_validate(account)
    return accountSchema
def get_account(db: Session, account_id: str):
    print("account_id in the service layer ", account_id)
    account = db.query(Account).filter(Account.id == account_id, Account.is_deleted == False).first()
    if not account:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Account not found"})
    print("account in the service layer ", account)
    accountSchema = AccountResponse.model_validate(account)
    print("accountSchema in the service layer ", accountSchema)


    return accountSchema

def get_transactions(db: Session, page_no: int, page_size: int, transaction_request):
    query = db.query(Transaction).filter(Transaction.account_id == transaction_request.account_id, Transaction.is_deleted == False)
    if transaction_request:
        if transaction_request.transaction_type:
            query = query.filter(Transaction.transaction_type == transaction_request.transaction_type)
        if transaction_request.transaction_date:
            query = query.filter(Transaction.transaction_date == transaction_request.transaction_date)
        if transaction_request.transaction_status:
            query = query.filter(Transaction.transaction_status == transaction_request.transaction_status)
    query = query.order_by(desc(Transaction.transaction_date))
    total = query.count()
    transactions = query.limit(page_size).offset((page_no - 1) * page_size).all()

    return {"total": total, "transactions": transactions}