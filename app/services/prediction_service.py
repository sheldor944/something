from datetime import datetime
from fastapi import UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from models.user import User
from models.trade import Prediction
from models.stock import Stock
from schemas.requests.prediction import PredictionRequest, PredictionFilter
from schemas.responses.prediction import  PredictionResponse


# model will create the prediction
def create_prediction(db: Session, prediction_request: PredictionRequest, user: User):
    prediction = Prediction(**prediction_request.model_dump())
    prediction.created_by = user.id
    db.add(prediction)
    db.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Prediction created successfully"})


# get the predictions by user 
def get_prediction(db: Session, prediction_filter : PredictionFilter):
    query = db.query(Prediction).filter(Prediction.is_deleted == False)
    if prediction_filter:
        if prediction_filter.prediction_id:
            query = query.filter(Prediction.id == prediction_filter.prediction_id)
        if prediction_filter.stock_id:
            query = query.filter(Prediction.stock_id == prediction_filter.stock_id)
        if prediction_filter.symbol:
            query = query.join(Stock).filter(Stock.symbol == prediction_filter.symbol)
        if prediction_filter.startDate:
            query = query.filter(Prediction.date >= prediction_filter.startDate)
        if prediction_filter.endDate:
            query = query.filter(Prediction.date <= prediction_filter.endDate)

    
    items = query.all()
    return [PredictionResponse.model_validate(item) for item in items]


 
    