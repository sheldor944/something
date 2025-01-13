import os
from datetime import datetime
from fastapi import File, UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from models.image import Image

def upload_image(db:Session, file:UploadFile=File(...)):
    try:
        file_location = f"media/images/{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
        with open(file_location, "wb") as file_object:
            file_object.write(file.file.read())

        image = Image(url=file_location)
        db.add(image)
        db.commit()
        db.refresh(image)

        return image
    
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content={"message":str(e)})
    
def get_images(db:Session):
    images = db.query(Image).all()
    if not images:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content={"message":"No Image found"})
    
    return images

def delete_image(db:Session, image_id:str):
    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content={"message":"Image not found"})
    
    if(os.path.exists(image.url)):
        os.remove(image.url)
    
    db.delete(image)
    db.commit()

    return JSONResponse(status_code=status.HTTP_200_OK,content={"message":"Image deleted successfully"})