from datetime import datetime
from fastapi import UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from models.user import User
from models.event import Event
from schemas.requests.event import EventRequest, EventUpdateRequest
from schemas.responses.event import  EventResponse
from services import image_service
from utils.pagination import create_paginated_response
from utils.query_filter_builder import QueryFilterBuilder

def create_event (db: Session, create_event: EventRequest, user:User, banner:UploadFile):
    event = Event(**create_event.model_dump())
    event.banner = image_service.upload_image(db, banner)
    event.created_by = user.id
    db.add(event)
    db.commit()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Event created successfully"}) 

def update_event(db: Session, event_id: str, update_event: EventUpdateRequest, user: User, banner: UploadFile = None):
    event = db.query(Event).filter(Event.id == event_id, Event.is_deleted==False).first()
    if not event:
        raise JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Event not found"})

    event_data = update_event.model_dump(exclude_unset=True)
    for key, value in event_data.items():
        setattr(event, key, value)

    if banner:
        if(event.banner):
            img_id = event.banner.id
        event.banner = image_service.upload_image(db, banner)
        if img_id:
            image_service.delete_image(db, img_id)

    event.last_updated_by = user.id
    db.commit()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Event updated successfully"})

def get_event(db:Session, event_id:str):
    event = db.query(Event).filter(Event.id == event_id, Event.is_deleted==False).first()
    if not event:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content={"message":"Event not found"})
    
    eventSchema = EventResponse.model_validate(event)
    
    return eventSchema

def get_upcoming_events(db:Session):
    events = db.query(Event).filter(Event.end_date >= datetime.now(),Event.is_deleted==False).order_by(Event.start_date.asc(),Event.created_at.asc()).all()
    return events

def get_past_events(db: Session, page: int, page_size: int):
    query = db.query(Event).filter(Event.end_date < datetime.now(), Event.is_deleted == False).order_by(Event.start_date.asc(),Event.created_at.asc()) 
    return create_paginated_response(query, page, page_size, EventResponse)

def get_events(db:Session, page:int, page_size:int, title:str, description:str, venue:str):
    query = db.query(Event).filter(Event.is_deleted==False)
    query = (
        QueryFilterBuilder(query, Event)
        .contains_filter("title", title)
        .contains_filter("description", description)
        .contains_filter("venue", venue)
        .build()
    )

    return create_paginated_response(query, page, page_size, EventResponse)
    
def delete_event(db: Session, event_id: str, user: User):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Event not found"})

    event.is_deleted = True
    event.last_update_by = user.id

    db.commit()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Event deleted successfully"})

