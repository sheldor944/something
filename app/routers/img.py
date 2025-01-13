from fastapi import APIRouter, File, UploadFile,status
from services import image_service
from dependency import get_db_session

# for testing purposes
router = APIRouter(
    prefix="/img",
    tags=["image"]
)

@router.post("/upload",status_code=status.HTTP_201_CREATED)
def upload_image(db:get_db_session,file:UploadFile=File(...)):
    return image_service.upload_image(db,file)

@router.get("/all")
def get_images(db:get_db_session):
    return image_service.get_images(db)

@router.delete("/{image_id}")
def delete_image(db:get_db_session,image_id:str):
    return image_service.delete_image(db,image_id)
