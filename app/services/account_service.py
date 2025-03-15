from datetime import datetime
from fastapi import UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from models.user import User
from models.trade import Trade
from schemas.requests.accounts import AccountRequest, AccountUpdateRequest
from schemas.responses.account import  AccountResponse
from models.account import Account, AutomatedAccount
from models.account import Transaction


def create_account(db: Session, user: User, account_request: AccountRequest):
    account = Account(**account_request.model_dump())
    account.user_id = user.id
    account.created_by = user.id
    db.add(account)
    db.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Account created successfully"})

def update_account(db: Session, user: User, account_update_request: AccountUpdateRequest):
    user_id = user.id
    account = db.query(Account).filter(Account.user_id == user_id, Account.is_deleted == False).first()
    if not account:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Account not found"})
    if account_update_request.amount is not None:
        print("account.balance before update ", account.balance)
        if account_update_request.modificationType == True:
            account.balance = account.balance + account_update_request.amount
        else:
            account.balance = account.balance - account_update_request.amount
    
    # if account_update_request.automated_balance is not None:
    #     automated_account = db.query(AutomatedAccount).filter(AutomatedAccount.account_id == account.id, AutomatedAccount.is_deleted == False).first()
    #     if not automated_account:
    #         return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Automated Account not found"})
    #     print("automated_account.balance before update ", automated_account.balance)
    #     if account_update_request.modificationTypeAutomated == True:
    #         automated_account.balance = automated_account.balance + account_update_request.automated_balance
            
    #     else:
    #         automated_account.balance = automated_account.balance - account_update_request.automated_balance

    #     account.automated_balance = automated_account.balance


   
    db.commit()
    accountSchema = AccountResponse.model_validate(account)
    return accountSchema
def get_account(db: Session, user: User):
    print("account_id in the service layer ", user.id)
    account_id = user.id
    account = db.query(Account).filter(Account.id == account_id, Account.is_deleted == False).first()
    if not account:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Account not found"})
    print("account in the service layer ", account)
    accountSchema = AccountResponse.model_validate(account)
    print("accountSchema in the service layer ", accountSchema)


    return accountSchema

def get_transactions(db: Session, user: User,  page_no: int, page_size: int, transaction_request):
    account = db.query(Account).filter(Account.user_id == user.id, Account.is_deleted == False).first()
    if not account:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Account not found"})
    
    query = db.query(Transaction).filter(Transaction.account_id == account.id, Transaction.is_deleted == False)
    if transaction_request:
        if transaction_request.transaction_type:
            query = query.filter(Transaction.transaction_type == transaction_request.transaction_type)
        if transaction_request.transaction_date:
            query = query.filter(Transaction.transaction_date == transaction_request.transaction_date)
        if transaction_request.transaction_status:
            query = query.filter(Transaction.transaction_status == transaction_request.transaction_status)
        if transaction_request.symbol:
            query = query.filter(Transaction.symbol == transaction_request.symbol)
        if transaction_request.transaction_done_by:
            query = query.filter(Transaction.transaction_done_by == transaction_request.transaction_done_by)
    query = query.order_by(desc(Transaction.transaction_date))
    total = query.count()
    transactions = query.limit(page_size).offset((page_no - 1) * page_size).all()

    return {"total": total, "transactions": transactions}

def create_automated_account(db: Session, user: User,  automated_account_request):

    automated_account = AutomatedAccount(**automated_account_request.model_dump())
    account = db.query(Account).filter(Account.user_id == user.id, Account.is_deleted == False).first()
    automated_account.account_id = account.id
    if not account:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Account not found"})
    if account.balance < automated_account_request.balance:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Insufficient balance in the account"})
    account.balance = account.balance - automated_account_request.balance
    account.automated_balance = automated_account_request.balance
    automated_account.created_by = user.id
    db.add(automated_account)
    db.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Automated Account created successfully"})

def update_automated_account(db: Session, user: User, automated_account_request):
    account = db.query(Account).filter(Account.user_id == user.id, Account.is_deleted == False).first()
    if not account:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Account not found"})
    automated_account = db.query(AutomatedAccount).filter(AutomatedAccount.account_id == account.id, AutomatedAccount.is_deleted == False).first()
    if not automated_account:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Automated Account not found"})
    if automated_account_request.amount is not None:
       
        print("automated_account.balance before update ", automated_account.balance)
        if automated_account_request.modificationType == True:
            if account.balance < automated_account_request.amount:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Insufficient balance in the account"})
            automated_account.balance = automated_account.balance + automated_account_request.amount
            account.balance = account.balance - automated_account_request.amount
        else:
            if automated_account.balance < automated_account_request.amount:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Insufficient balance in the automated account"})
            automated_account.balance = automated_account.balance - automated_account_request.amount
            account.balance = account.balance + automated_account_request.amount

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Automated Account updated successfully"})