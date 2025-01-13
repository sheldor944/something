from fastapi import APIRouter, File, UploadFile, status, Query
from schemas.requests.user import ProfileUpdateRequest
from services import profile_service
from dependency import get_db_session, get_current_user

router = APIRouter(
    tags=["profile"]
)

@router.put("/profile")
def update_profile_info(db:get_db_session,profileInfoUpdate:ProfileUpdateRequest,user:get_current_user):
    return profile_service.update_profile_info(db,profileInfoUpdate,user.id)

@router.put("/profile/picture")
def update_profile_picture(db:get_db_session,user:get_current_user,file:UploadFile=File(...)):
    return profile_service.update_profile_picture(db,user.id,file)

@router.get("/profile")
def get_profile_info(db:get_db_session,user:get_current_user):
    return profile_service.get_profile_info(db,user.id)

@router.get("/profile/all")
def get_all_profiles(
    db:get_db_session,
    page_no: int = Query(1, ge=1, description="Page number"), 
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page")
    ):
    return profile_service.get_all_profiles(db, page_no, page_size)

@router.get("/profile/{user_id}")
def get_profile_info(db:get_db_session,user_id:str):
    return profile_service.get_profile_info(db,user_id)

