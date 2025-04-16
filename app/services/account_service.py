from datetime import datetime
from fastapi import UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from models.user import User
from models.trade import Trade
from schemas.requests.accounts import AccountRequest, AccountUpdateRequest, AutomatedAccountUpdateRequest, AutomatedHandlerRequest
from schemas.responses.account import  AccountResponse, AutomatedAccountHandlerResponse, AutomatedAccountResponse
from models.account import Account, AutomatedAccount, AutomatedHandler
from models.account import Transaction
from automation_handler.automated_handler_thread import AutomatedHandlerThread


def create_account(db: Session, user: User, account_request: AccountRequest):
    print(f"account_req {account_request} ")
    account = db.query(Account).filter(Account.user_id == user.id, Account.is_deleted == False).first()
    if account:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Account already exists"})
    account = Account(**account_request.model_dump())
    account.automated_balance = 0
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
    print("===================================")
    account = db.query(Account).filter(Account.user_id == user.id, Account.is_deleted == False).first()
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

# def update_automated_account(db: Session, user: User, automated_account_request : AutomatedAccountUpdateRequest):
#     account = db.query(Account).filter(Account.user_id == user.id, Account.is_deleted == False).first()
#     if not account:
#         return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Account not found"})
#     automated_account = db.query(AutomatedAccount).filter(AutomatedAccount.account_id == account.id, AutomatedAccount.is_deleted == False).first()
#     if not automated_account:
#         return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Automated Account not found"})
#     if automated_account_request.amount is not None:
       
#         print("automated_account.balance before update ", automated_account.balance)
#         if automated_account_request.modificationTypeAutomated == True:
#             if account.balance < automated_account_request.amount:
#                 return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Insufficient balance in the account"})
#             print("here")
#             automated_account.balance = automated_account.balance + automated_account_request.amount
#             account.balance = account.balance - automated_account_request.amount
#             print("automated_account.balance after update ", automated_account.balance)
#             print("account.balance after update ", account.balance)
#             db.commit()
#         # else:
#             if automated_account.balance < automated_account_request.amount:
#                 return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Insufficient balance in the automated account"})
#             automated_account.balance = automated_account.balance - automated_account_request.amount
#             account.balance = account.balance + automated_account_request.amount
#             db.commit()
#     db.flush()
#     db.commit()
#     return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Automated Account updated successfully"})

from sqlalchemy.exc import SQLAlchemyError

def update_automated_account(db: Session, user: User, automated_account_request: AutomatedAccountUpdateRequest):
    try:
        account = db.query(Account).filter(Account.user_id == user.id, Account.is_deleted == False).first()
        if not account:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Account not found"})

        automated_account = db.query(AutomatedAccount).filter(AutomatedAccount.account_id == account.id, AutomatedAccount.is_deleted == False).first()
        if not automated_account:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Automated Account not found"})

        if automated_account_request.amount is not None:
            print("automated_account.balance before update ", automated_account.balance)
            if automated_account_request.modificationTypeAutomated:
                if account.balance < automated_account_request.amount:
                    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Insufficient balance in the account"})
                print("here")
                automated_account.balance += automated_account_request.amount
                account.balance -= automated_account_request.amount
                account.automated_balance = automated_account.balance

                db.flush()  # Ensure changes are sent to the database
                db.commit()  # Commit the transaction

            else:
                if automated_account.balance < automated_account_request.amount:
                    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Insufficient balance in the automated account"})
                automated_account.balance -= automated_account_request.amount
                account.balance += automated_account_request.amount
                account.automated_balance = automated_account.balance

            print("automated_account.balance after update ", automated_account.balance)
            print("account.balance after update ", account.balance)

            db.flush()  # Ensure changes are sent to the database
            db.commit()  # Commit the transaction

        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Automated Account updated successfully"})

    except SQLAlchemyError as e:
        db.rollback()  # Rollback in case of error
        print(f"Database error: {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Database error occurred"})

def create_automated_handler(db: Session, user: User, automated_handler_request: AutomatedHandlerRequest):
    print("int the handler mode ")
    account = db.query(Account).filter(Account.user_id == user.id, Account.is_deleted == False).first()
    if not account:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Account not found"})
    automated_account = db.query(AutomatedAccount).filter(AutomatedAccount.account_id == account.id, AutomatedAccount.is_deleted == False).first()
    if not automated_account:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Automated Account not found"})
    print(" found the account and automated account ")
    automated_handler = AutomatedHandler(**automated_handler_request.model_dump())
    automated_handler.automated_account_id = automated_account.id
    automated_handler.user = user
    automated_handler.created_by = user.id
    automated_handler.status = "ACTIVE"
    automated_handler.balance = automated_account.balance
    # Now start a thread for running automatically for trading, take the userId and automated_account_id, account_id


    db.add(automated_handler)
    db.commit()

    # Start the thread
    # thread = AutomatedHandlerThread(
    #     db_session=db,
    #     automated_handler_id=automated_handler.id,
    #     user_id=user.id,
    #     account_id=account.id
    # )
    # thread.start()


    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Automated Handler created successfully"})

def get_all_automated_handler(db: Session):
    
    print("in the service layer ")
    automated_handlers = db.query(AutomatedHandler).filter(AutomatedHandler.status == "ACTIVE",AutomatedHandler.is_deleted == False).all()
    # print("automated_handlers in the service layer ", automated_handlers)
    if not automated_handlers:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Automated Handler not found"})
    print("automated_handlers in the service layer ", automated_handlers)

    for automated_handler in automated_handlers:
        print(f"handler end time {automated_handler.end_time}")
        print(f"current time {datetime.now()}")
        if(automated_handler.end_time < datetime.now()):
            automated_handler.status = "INACTIVE"
            # db.add(automated_handler)
            db.commit()
   
    return [AutomatedAccountHandlerResponse.model_validate(automated_handler) for automated_handler in automated_handlers]

def get_automated_account_handler(db: Session, user: User):
    print("in the get automated account service layer ")
    account = db.query(Account).filter(Account.user_id == user.id, Account.is_deleted == False).first()
    if not account:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Account not found"})
    automated_account = db.query(AutomatedAccount).filter(AutomatedAccount.account_id == account.id, AutomatedAccount.is_deleted == False).first()
    if not automated_account:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Automated Account not found"})
    print("automated_account in the service layer ", automated_account)
    automated_handler = db.query(AutomatedHandler).filter(AutomatedHandler.automated_account_id == automated_account.id, AutomatedHandler.is_deleted == False).first()
    if not automated_handler:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Automated Handler not found"})
    print("automated_handler in the service layer ", automated_handler)
    automated_accountSchema = AutomatedAccountHandlerResponse.model_validate(automated_handler)
    print("automated_accountSchema in the service layer ", automated_accountSchema)

    return automated_accountSchema

def get_automated_account(db: Session, user: User):
    print("in the get automated account service layer ")
    account = db.query(Account).filter(Account.user_id == user.id, Account.is_deleted == False).first()
    if not account:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Account not found"})
    automated_account = db.query(AutomatedAccount).filter(AutomatedAccount.account_id == account.id, AutomatedAccount.is_deleted == False).first()
    if not automated_account:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Automated Account not found"})
    print("automated_account in the service layer ", automated_account)
    automated_accountSchema = AutomatedAccountResponse.model_validate(automated_account)
    print("automated_accountSchema in the service layer ", automated_accountSchema)

    return automated_accountSchema