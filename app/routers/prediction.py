from fastapi import APIRouter, File, UploadFile, Query, Depends
from schemas.requests.prediction import PredictionFilter, PredictionRequest
from services import prediction_service
from dependency import get_db_session, get_current_user

router = APIRouter(
    tags=["prediction"]
)

@router.post("/prediction")
def create_prediction(db: get_db_session, prediction_request: PredictionRequest , user: get_current_user):
    return prediction_service.create_prediction(db, prediction_request, user)

@router.get("/prediction")
def get_prediction(db: get_db_session, prediction_filter : PredictionFilter = Depends(None)):
    return prediction_service.get_prediction(db, prediction_filter)