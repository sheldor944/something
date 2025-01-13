from datetime import datetime
from fastapi import status, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
from models.image import Image
from models.user import Profile, User
from models.hall_of_fame import HallOfFame, people_in_hall_of_fame
from schemas.responses.user import ProfileResponse
from schemas.requests.hall_of_fame import HallOfFameRequest, HallOfFameUpdateRequest
from schemas.responses.hall_of_fame import HallOfFameResponse
from services import image_service
from utils.pagination import create_paginated_response
from utils.query_filter_builder import QueryFilterBuilder

def create_hall_of_fame (db: Session, user:User, create_hof: HallOfFameRequest):
    hof = HallOfFame(**create_hof.model_dump())
    hof.created_by = user.id
    db.add(hof)
    db.commit()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Hall Of Fame created successfully"}) 

def update_hall_of_fame(db:Session, user:User, hof_id:str, update_hof:HallOfFameUpdateRequest):
    hof = db.query(HallOfFame).filter(HallOfFame.id == hof_id,HallOfFame.is_deleted==False).first()
    if not hof:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Hall Of Fame not found"})

    hof_data = update_hof.model_dump(exclude_unset=True)
    for key, value in hof_data.items():
        setattr(hof, key, value)

    hof.last_updated_by = user.id  
    db.commit()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Hall Of Fame updated successfully"})

def get_hall_of_fame(db:Session, hof_id:str):
    hof = db.query(HallOfFame).filter(HallOfFame.id == hof_id, HallOfFame.is_deleted==False).first()
    if not hof:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content={"message":"Hall Of Fame not found"})
    
    hofSchema = HallOfFameResponse.model_validate(hof)

    return hofSchema

def get_hall_of_fames(db:Session, page:int, page_size:int, title:str, description:str):
    query = db.query(HallOfFame).filter(HallOfFame.is_deleted==False)
    query = (
        QueryFilterBuilder(query, HallOfFame)
        .contains_filter("title", title)
        .contains_filter("title", title)
        .contains_filter("description", description)
        .build()
    )

    return create_paginated_response(query, page, page_size, HallOfFameResponse)

def delete_hall_of_fame(db: Session, hof_id: str, user: User):
    hof = db.query(HallOfFame).filter(HallOfFame.id == hof_id).first()
    if not hof:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Hall Of Fame not found"})
    hof.is_deleted = True
    hof.last_update_by = user.id
    db.commit()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Hall Of Fame deleted successfully"})

def add_image_to_hof(db: Session, user:User, hof_id: str, image: UploadFile):
    hof = db.query(HallOfFame).filter(HallOfFame.id == hof_id, HallOfFame.is_deleted == False).first()
    if not hof:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Hall Of Fame not found"})
    
    image = image_service.upload_image(db, image)
    hof.images.append(image)
    hof.last_updated_at = datetime.now()
    db.commit()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Image added to Hall Of Fame successfully"})

def delete_image_from_hof(db: Session, user:User, hof_id: str, image_id: str):
    hof = db.query(HallOfFame).filter(HallOfFame.id == hof_id, HallOfFame.is_deleted == False).first()
    if not hof:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Hall Of Fame not found"})
    
    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Image not found"})
    
    hof.images.remove(image)
    hof.last_updated_by = user.id
    image_service.delete_image(db, image_id)
    db.commit()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Image deleted from Hall Of Fame successfully"})

def add_user_to_hof(db:Session, update_user:User, hof_id:str, user_id:str):
    hof = db.query(HallOfFame).filter(HallOfFame.id == hof_id, HallOfFame.is_deleted == False).first()
    if not hof:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Hall Of Fame not found"})
    
    user = db.query(User).filter(User.id == user_id, User.is_deleted == False).first()
    if not user:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "User not found"})
    
    hof.people.append(user)
    hof.last_updated_by = update_user.id
    db.commit()
   
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "User added to Hall Of Fame successfully"})

def remove_user_from_hof(db:Session, update_user:User, hof_id:str, user_id:str):
    hof = db.query(HallOfFame).filter(HallOfFame.id == hof_id, HallOfFame.is_deleted == False).first()
    if not hof:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Hall Of Fame not found"})
    
    user = db.query(User).filter(User.id == user_id, User.is_deleted == False).first()
    if not user:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "User not found"})
    
    hof.people.remove(user)
    hof.last_updated_by = update_user.id
    db.commit()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "User removed from Hall Of Fame successfully"})

def get_unassigned_users(db: Session, hof_id: str, page: int, page_size: int):
    hof = db.query(HallOfFame).filter(HallOfFame.id == hof_id, HallOfFame.is_deleted == False).first()
    if not hof:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Hall Of Fame not found"})

    subquery = db.query(people_in_hall_of_fame.c.user_id).filter(people_in_hall_of_fame.c.hall_of_fame_id == hof_id).subquery()

    query = db.query(Profile).filter(~exists().where(Profile.user_id == subquery.c.user_id))

    return create_paginated_response(query, page, page_size, ProfileResponse)