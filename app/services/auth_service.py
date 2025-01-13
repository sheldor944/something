from datetime import datetime
from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from models.user import User, UserSession, Profile
from schemas.requests.user import UserSignUp, UserSignIn
from utils import oauth2, agent_parse


def sign_up_user(userSchema: UserSignUp, db: Session):
    existed_user = db.query(User).filter(User.email == userSchema.email).first()
    if existed_user:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "User with email already exists"})
    
    existed_user = db.query(User).filter(User.user_name == userSchema.user_name).first()
    if existed_user:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "User with user name already exists"})
    
    if len(userSchema.user_name)<3 or not userSchema.user_name.isalnum():
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "User name must be alphanumeric and at least 3 characters long"})
    
    # if not oauth2.is_strong_password(userSchema.password):
    #     return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number and one special character"})

    user = User(**userSchema.model_dump())
    user.password_salt = oauth2.generate_salt()
    user.password = oauth2.hash(user.password+" "+user.password_salt)

    db.add(user)
    db.commit()
    db.refresh(user)
    profile = Profile(user_id=user.id)
    db.add(profile)
    db.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "User created successfully"})

def sign_in_user(userSchema: UserSignIn, db: Session, request: Request):
    user = db.query(User).filter(User.email == userSchema.email).first()

    user_agent = request.headers.get("User-Agent")

    ip_address = request.client.host if request.client else '0.0.0.0'

    user_agent_info = agent_parse.parse_user_agent(user_agent)

    if not user:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "User not found"})

    if not oauth2.verify(userSchema.password+" "+user.password_salt, user.password):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "Invalid password"})

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

    return {
        "user_id": user.id,
        "role": user.role,
        "token": token
    }

def get_user_sessions(db: Session, user_id: str):
    user_sessions = db.query(UserSession).filter(UserSession.user_id == user_id, UserSession.is_deleted==False).all()
    return user_sessions

def log_out(db: Session, user_session_id: str):
    user_session = db.query(UserSession).filter(UserSession.id == user_session_id).first()

    if not user_session:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Session not found"})

    user_session.is_deleted = True
    user_session.last_updated_at = datetime.now()
    db.commit()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Logged out successfully"})

def log_out_current(db: Session, token: str):
    user_session = db.query(UserSession).filter(UserSession.token == token).first()

    if not user_session:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Session not found"})

    user_session.is_deleted = True
    user_session.last_updated_at = datetime.now()
    db.commit()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Logged out successfully"})

def logout_all(db: Session, user_id: str):
    user_sessions = db.query(UserSession).filter(UserSession.user_id == user_id).all()

    for user_session in user_sessions:
        user_session.is_deleted = True
        user_session.last_updated_at = datetime.now()

    db.commit()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Logged out from all devices successfully"})

def isLoggedIn(db: Session, token: str):
    user_session = db.query(UserSession).filter(UserSession.token == token,UserSession.is_deleted==True).first()

    if not user_session:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Logged out"})

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Logged in"})

# testing purpose
def delete_user(db: Session, user_id: str):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "User not found"})
    
    user_sessions = db.query(UserSession).filter(UserSession.user_id == user_id).all()

    if user_sessions:
        for user_session in user_sessions:
            db.delete(user_session)
    db.delete(user)
    db.commit()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "User deleted successfully"})