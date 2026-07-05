"""
Prediction API routes.
"""
from fastapi import APIRouter

from app.schemas.prediction import PredictionRequest
from app.services import prediction_service

router = APIRouter(prefix="/api/predict", tags=["Prediction"])
history_router = APIRouter(prefix="/api/predictions", tags=["Prediction History"])


@router.post("")
async def predict(payload: PredictionRequest):
    return await prediction_service.run_prediction(payload)


@history_router.get("")
async def list_predictions(limit: int = 200):
    return await prediction_service.list_predictions(limit=limit)


@history_router.get("/{equipment_id}")
async def list_predictions_for_equipment(equipment_id: str, limit: int = 100):
    return await prediction_service.list_predictions_for_equipment(equipment_id, limit=limit)
