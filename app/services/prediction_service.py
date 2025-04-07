from datetime import datetime
from fastapi import UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from models.user import User
from models.trade import Prediction, CurrentPrediction
from models.stock import Stock
from schemas.requests.prediction import PredictionRequest, PredictionFilter, CurrentPredictionRequest
from schemas.responses.prediction import  PredictionResponse, CurrentPredictionResponse
import pandas as pd
from datetime import datetime
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List
import os 


# model will create the prediction
def create_prediction(db: Session, prediction_request: PredictionRequest):
    print("here")
    user = db.query(User).filter(User.is_deleted == False).first()
    print("got a user")
    prediction = Prediction(**prediction_request.model_dump())
    prediction.created_by = user.id
    latest_current_prediction = db.query(CurrentPrediction).filter(CurrentPrediction.is_deleted == False).order_by(desc(CurrentPrediction.date)).first()
    if latest_current_prediction:
        latest_current_prediction.is_deleted = True
        
    currentPredictionRequest = CurrentPredictionRequest(
        symbol=prediction.symbol,
        opening_price=prediction.opening_price,
        closing_price=prediction.closing_price,
        high_price=prediction.high_price,
        low_price=prediction.low_price,
        volume=prediction.volume,
        date=prediction.date,
        prediction_direction=prediction.prediction_direction
    )
    currentPrediction = CurrentPrediction(**currentPredictionRequest.model_dump())
    currentPrediction.created_by = user.id
    db.add(currentPrediction)

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


 
    



def add_csv_predictions_to_db(db: Session, user: User, csv_file_path: str = "app/services/predictions_with_direction.csv"):
    """
    Read predictions from CSV file and add them to the database
    """
    try:
        # Read CSV file
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        absolute_path = os.path.join(base_dir, "services", "predictions_with_direction.csv")
        
        print(f"Reading predictions from {absolute_path}")
        df = pd.read_csv(absolute_path)
        # Convert predictions to list of PredictionRequest objects
        predictions: List[PredictionRequest] = []
        
        for _, row in df.iterrows():
            prediction = PredictionRequest(
                stock_id= "8deb8028-5bed-4bcd-88f3-5a12c41c7aac",
                symbol="XAUUSD",  # Add your default symbol here
                opening_price=0,  # Using Price as opening_price
                closing_price=row['Price'],  # Using Price as closing_price
                high_price=0,    # Using Price as high_price
                low_price=0,     # Using Price as low_price
                volume=0.0,                 # Default volume, adjust as needed
                date=datetime.strptime(row['Time'], '%Y-%m-%d %H:%M:%S'),
                prediction_direction=bool(row['Direction'])
            )
            predictions.append(prediction)
        
        # Add each prediction to the database
        for prediction_request in predictions:
            prediction = Prediction(**prediction_request.model_dump())
            prediction.created_by = user.id
            db.add(prediction)
        
        # Commit all changes at once
        db.commit()
        
        return {"message": f"Successfully added {len(predictions)} predictions to database"}
    
    except Exception as e:
        db.rollback()
        return {"error": f"Failed to add predictions: {str(e)}"}
    

def create_current_prediction(db: Session, prediction_request: PredictionRequest, user: User):
    prediction = CurrentPrediction(**prediction_request.model_dump())
    prediction.created_by = user.id
    db.add(prediction)
    db.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Prediction created successfully"})

def get_current_prediction(db: Session):
    query = db.query(CurrentPrediction).filter(CurrentPrediction.is_deleted == False)
    items = query.all()
    return [CurrentPredictionResponse.model_validate(item) for item in items]

def delete_current_prediction(db: Session, prediction_id: str):
    prediction = db.query(CurrentPrediction).filter(CurrentPrediction.id == prediction_id).first()
    if prediction:
        prediction.is_deleted = True
        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Prediction deleted successfully"})
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Prediction not found"})
