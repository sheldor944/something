from fastapi import APIRouter, File, UploadFile, Query
from schemas.requests.hall_of_fame import HallOfFameRequest, HallOfFameUpdateRequest
from services import hall_of_fame_service
from dependency import get_db_session, get_current_user

router = APIRouter(
    tags=["hall_of_fame"]
)

@router.post("/hof")  
def create_hall_of_fame(db: get_db_session, user: get_current_user, create_hof: HallOfFameRequest):
    return hall_of_fame_service.create_hall_of_fame(db, user, create_hof)

@router.put("/hof/{hof_id}")
def update_hall_of_fame(db: get_db_session, user: get_current_user, hof_id: str, update_hof: HallOfFameUpdateRequest):
    return hall_of_fame_service.update_hall_of_fame(db, user, hof_id, update_hof)

@router.get("/hofs")
def get_hall_of_fames(
    db: get_db_session, 
    page_no: int = Query(1, ge=1, description="Page number"), 
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    title: str = Query(None, description="Filter by title"),
    description: str = Query(None, description="Filter by description")
    ):
    return hall_of_fame_service.get_hall_of_fames(db, page_no, page_size, title, description)

@router.get("/hof/{hof_id}")
def get_hall_of_fame(db: get_db_session, hof_id: str):
    return hall_of_fame_service.get_hall_of_fame(db, hof_id)

@router.delete("/hof/{hof_id}")
def delete_hall_of_fame(db: get_db_session, user: get_current_user, hof_id: str):
    return hall_of_fame_service.delete_hall_of_fame(db, hof_id, user)

@router.post("/hof/{hof_id}/image")
def add_image_to_hof(db: get_db_session, user:get_current_user, hof_id: str, image: UploadFile = File(...)):
    return hall_of_fame_service.add_image_to_hof(db, user, hof_id, image)

@router.delete("/hof/{hof_id}/image/{image_id}")
def delete_image_from_hof(db: get_db_session, user:get_current_user, hof_id: str, image_id: str):
    return hall_of_fame_service.delete_image_from_hof(db, user, hof_id, image_id)

@router.post("/hof/{hof_id}/{user_id}")
def add_user_to_hof(db: get_db_session, user: get_current_user, hof_id: str, user_id: str):
    return hall_of_fame_service.add_user_to_hof(db, user, hof_id, user_id)

@router.delete("/hof/{hof_id}/{user_id}")
def remove_user_from_hof(db: get_db_session, user:get_current_user, hof_id: str, user_id: str):
    return hall_of_fame_service.remove_user_from_hof(db, user, hof_id, user_id)

@router.get("/hof/{hof_id}/unassigned")
def get_unassigned_users(db: get_db_session,
    hof_id: str,
    page_no: int = Query(1, ge=1, description="Page number"), 
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page")
    ):
    return hall_of_fame_service.get_unassigned_users(db, hof_id, page_no, page_size)




