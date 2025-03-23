from fastapi import APIRouter, File, UploadFile, Query, Depends
from schemas.requests.accounts import  AccountRequest, TransactionRequest, AccountUpdateRequest, AutomatedAccountRequest, AutomatedHandlerRequest, AutomatedAccountUpdateRequest
from services import account_service
from dependency import get_db_session, get_current_user

router = APIRouter(
    tags=["accounts"]
)

@router.post("/account")
def create_account(db: get_db_session, user: get_current_user, account_request: AccountRequest):
    return account_service.create_account(db, user, account_request)

@router.get("/user_account")
def get_account(db: get_db_session, user: get_current_user ):
    # print("account_id", account_id)
    return account_service.get_account(db, user)

@router.get("/transactions")
def get_transactions(db: get_db_session,
                     user: get_current_user,
                    page_no: int = Query(1, ge=1, description="Page number"), 
                    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
                    transaction_request : TransactionRequest = Depends(),
                    ):
    return account_service.get_transactions(db, user, page_no, page_size, transaction_request)

@router.put("/update_account")
def update_account(db: get_db_session, user: get_current_user, account_update_request: AccountUpdateRequest):
    print("account_update_request in the router ", account_update_request)
    return account_service.update_account(db, user, account_update_request)

@router.post("/create_automated_account")
def create_automated_account(db: get_db_session, user: get_current_user,  automated_account_request: AutomatedAccountRequest):
    return account_service.create_automated_account(db, user,  automated_account_request)

@router.put("/update_automated_account")
def update_automated_account(db: get_db_session, user: get_current_user, automated_account_request: AutomatedAccountUpdateRequest):
    return account_service.update_automated_account(db, user, automated_account_request)

@router.post("/create_automated_handler")
def create_automated_handler(db: get_db_session, user: get_current_user, automated_handler_request: AutomatedHandlerRequest):
    print("automated_handler_request in the router ", automated_handler_request)
    return account_service.create_automated_handler(db, user, automated_handler_request)