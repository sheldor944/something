from fastapi import APIRouter, File, UploadFile, Query, Depends
from schemas.requests.accounts import  AccountRequest, TransactionRequest, AccountUpdateRequest  
from services import account_service
from dependency import get_db_session, get_current_user

router = APIRouter(
    tags=["accounts"]
)

@router.post("/account")
def create_account(db: get_db_session, user: get_current_user, account_request: AccountRequest):
    return account_service.create_account(db, user, account_request)

@router.get("/account/{account_id}")
def get_account(db: get_db_session, account_id: str):
    print("account_id", account_id)
    return account_service.get_account(db, account_id)

@router.get("/transactions")
def get_transactions(db: get_db_session,
                    page_no: int = Query(1, ge=1, description="Page number"), 
                    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
                    transaction_request : TransactionRequest = Depends()):
    return account_service.get_transactions(db, page_no, page_size, transaction_request)

@router.put("/account/{user_id}")
def update_account(db: get_db_session, user_id: str, account_update_request: AccountUpdateRequest):
    print("account_update_request in the router ", account_update_request)
    return account_service.update_account(db, user_id, account_update_request)
