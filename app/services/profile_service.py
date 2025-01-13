from datetime import datetime
from fastapi import UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from models.user import Profile
from schemas.requests.user import ProfileUpdateRequest
from schemas.responses.user import ProfileResponse
from services import image_service
from utils.pagination import create_paginated_response

def update_profile_info(db: Session, profileInfoUpdate: ProfileUpdateRequest, user_id: str):
    profile = db.query(Profile).filter(Profile.user_id == user_id,Profile.is_deleted==False).first()
    if not profile:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Profile not found"})

    profile_data = profileInfoUpdate.model_dump(exclude_unset=True)
    for key, value in profile_data.items():
        setattr(profile, key, value)

    db.commit()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Profile updated successfully"})

def update_profile_picture(db: Session, user_id: str, file:UploadFile):

    profile = db.query(Profile).filter(Profile.user_id == user_id, Profile.is_deleted==False).first()

    if not profile:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Profile not found"})
    if not file:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "No file provided"})

    del_image = profile.image
    profile.image = image_service.upload_image(db, file)

    if del_image:
        image_service.delete_image(db, del_image.id)
    
    db.commit()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Profile picture updated successfully"}) 

def get_profile_info(db: Session, user_id: str):
    profile = db.query(Profile).filter(Profile.user_id == user_id, Profile.is_deleted==False).first()
    if not profile:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Profile not found"})
    
    profile_schema = ProfileResponse.model_validate(profile)
    return profile_schema

def get_all_profiles(db: Session, page_no: int, page_size: int):
    query = db.query(Profile).filter(Profile.is_deleted==False)

    return create_paginated_response(query, page_no, page_size, ProfileResponse)