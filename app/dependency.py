from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
import db
from utils import oauth2
from models.user import User

get_db_session = Annotated[Session,Depends(db.get_db)]

get_current_user = Annotated[User,Depends(oauth2.get_current_user)]