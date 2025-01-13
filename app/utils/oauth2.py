import os
import re
import secrets
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
import db
from models.user import User


load_dotenv()

oauthScheme = OAuth2PasswordBearer(tokenUrl="api/v1/token")

pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("ALGO")
ACCESS_TOKEN_EXPIRE_MINUTES = 24*60

def hash(password:str):
    return pwdContext.hash(password)

def generate_salt():    
    return secrets.token_hex(16)

def is_strong_password(password: str) -> bool:
    # Define the regular expression for a strong password
    pattern = re.compile(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    )
    # Check if the password matches the pattern
    if pattern.match(password):
        return True
    else:
        return False

def verify(plainPassword, hashedPassword):
    return pwdContext.verify(plainPassword, hashedPassword)

def createAccessToken(data:dict):
    toEncode =data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    toEncode.update({"exp":expire})

    encodedJWT = jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)
    return encodedJWT

def verifyAccessToken(Token: str, credentialException):
    try:
        payload = jwt.decode(Token, SECRET_KEY, algorithms=[ALGORITHM])
        id : str =  payload.get("user_id")

        if id is None:
            raise credentialException
        return id
    except JWTError:
        raise credentialException
    
def get_current_user(token : str= Depends(oauthScheme), db: Session = Depends(db.get_db)):
    credentialException = HTTPException(status_code=404, 
                                        detail="Token is invalid",
                                        headers={"WWW-Authenticate":"Bearer"})
    
    id = verifyAccessToken(token, credentialException)
    user = db.query(User).filter(User.id == id).first()
    return user