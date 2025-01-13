from datetime import datetime
from fastapi import APIRouter, File, Form, UploadFile, status, Query
from fastapi.responses import JSONResponse
from schemas.requests.event import EventRequest, EventUpdateRequest
from services import event_service
from dependency import get_db_session, get_current_user

router = APIRouter(
    tags=["event"]
)

@router.post("/event")
def create_event(
    db: get_db_session,
    user: get_current_user,
    title: str = Form(...),
    description: str = Form(None),
    start_date: datetime = Form(...),
    end_date: datetime = Form(...),
    venue: str = Form(None),
    event_link: str = Form(...),
    banner: UploadFile = File(...)
):
   
    required_fields = [title, event_link, start_date, end_date]
    if any(field is None or field == "" for field in required_fields):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "All required fields must be provided"})

    if start_date > end_date:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Start date must be less than end date"})
    
    create_event = EventRequest(title=title, description=description, start_date=start_date, end_date=end_date, venue=venue, event_link=event_link)
    return event_service.create_event(db, create_event, user, banner)

@router.put("/event/{event_id}")
def update_event(
    db: get_db_session,
    user: get_current_user,
    event_id: str,
    title: str = Form(None),
    description: str = Form(None),
    start_date: datetime = Form(None),
    end_date: datetime = Form(None),
    venue: str = Form(None),
    event_link: str = Form(None),
    banner: UploadFile = File(None)
):
    update_event = EventUpdateRequest(title=title, description=description, start_date=start_date, end_date=end_date, venue=venue, event_link=event_link)
    return event_service.update_event(db, event_id, update_event, user, banner)

@router.get("/event/upcoming")
def get_upcoming_events(db: get_db_session):
    return event_service.get_upcoming_events(db)

@router.get("/event/past")
def get_past_events(
    db: get_db_session,
    page_no: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page")
):
    return event_service.get_past_events(db, page_no, page_size)

@router.get("/events")
def get_events(
    db: get_db_session,
    page_no: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    title: str = Query(None, description="Filter by event title"),
    description: str = Query(None, description="Filter by event description"),
    venue: str = Query(None, description="Filter by event venue"),
    ):
    return event_service.get_events(db, page_no, page_size, title, description, venue)

@router.get("/event/{event_id}")
def get_event(db: get_db_session, event_id: str):
    return event_service.get_event(db, event_id)

@router.delete("/event/{event_id}")
def delete_event(db: get_db_session, user:get_current_user, event_id: str):
    return event_service.delete_event(db, event_id, user)