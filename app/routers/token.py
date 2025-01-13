from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter,status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import db
from utils import oauth2, agent_parse
from models.user import UserSession, User
from schemas.responses.user import TokenBasic

router = APIRouter()

@router.post("/token")
async def login_for_access_token(request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db:Session = Depends(db.get_db)
) -> TokenBasic:
    
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not oauth2.verify(form_data.password+" "+user.password_salt, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_agent = request.headers.get("User-Agent")
    
    ip_address = request.client.host if request.client else '0.0.0.0'   

    user_agent_info = agent_parse.parse_user_agent(user_agent)

    user_session = db.query(UserSession).filter(UserSession.user_id == user.id, UserSession.os==user_agent_info['os'],UserSession.device==user_agent_info['device'],UserSession.browser==user_agent_info['browser']).first()

    if not user_session:
        token = oauth2.createAccessToken({
            "user_id":str(user.id),
            "user_name":user.user_name,
            "email":user.email,
            "role":user.role,
            "ip_address":ip_address,
            "os":user_agent_info['os'],
            "device":user_agent_info['device'],
            "browser":user_agent_info['browser']
        })
        user_session = UserSession(user_id=user.id, ip_address=ip_address, os=user_agent_info['os'], device=user_agent_info['device'], browser=user_agent_info['browser'], token=token)

        db.add(user_session)
        db.commit()

    

    jwt_token = TokenBasic(access_token=user_session.token, token_type="bearer")

    return jwt_token