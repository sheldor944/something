from fastapi import APIRouter, Depends, Request, status
from schemas.requests.user import UserSignUp, UserSignIn
from schemas.responses.user import UserSessionResponse
from services import auth_service
from dependency import get_db_session
from utils import oauth2

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/signup")
def sign_up(userSchema:UserSignUp,db:get_db_session):
    return auth_service.sign_up_user(userSchema,db)

@router.post("/signin",status_code=status.HTTP_200_OK)
def sign_in(userSchema:UserSignIn,db:get_db_session, request:Request):
    return auth_service.sign_in_user(userSchema,db,request)

@router.get("/loginfos/{user_id}",response_model=list[UserSessionResponse])
def get_loginfos(db:get_db_session,user_id:str):
    return auth_service.get_user_sessions(db,user_id)

@router.delete("/logout/current")
def log_out_current(db:get_db_session,token:str = Depends(oauth2.oauthScheme)):
    return auth_service.log_out_current(db,token)

@router.delete("/logout/{user_session_id}")
def log_out(db:get_db_session, user_session_id:str):
    return auth_service.log_out(db, user_session_id)

@router.delete("/logout/all/{user_id}")
def logout_all(db:get_db_session,user_id:str):
    return auth_service.logout_all(db,user_id)

@router.get("/isLogged")
def is_logged(db:get_db_session,token:str = Depends(oauth2.oauthScheme)):
    return auth_service.isLoggedIn(db,token)

# for testing
@router.delete("/{user_id}")
def delete_user(db:get_db_session,user_id:str):
    return auth_service.delete_user(db,user_id)







