"""
Standalone AI recommendation endpoint — lets the frontend request maintenance
advice directly from sensor values without necessarily running/saving a full
prediction record.
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from app.services import ai_service, equipment_service
from app.utils.health_logic import evaluate_sensor_reading

router = APIRouter(prefix="/api/ai", tags=["AI Maintenance Agent"])


class AIRecommendationRequest(BaseModel):
    equipment_id: str
    temperature: float
    vibration: float
    pressure: float


@router.post("/recommendation")
async def get_ai_recommendation(payload: AIRecommendationRequest):
    equipment = await equipment_service.get_equipment_by_equipment_id(payload.equipment_id)
    equipment_name = equipment["equipment_name"] if equipment else payload.equipment_id

    health_score, risk_level, failure_probability, _ = evaluate_sensor_reading(
        payload.temperature, payload.vibration, payload.pressure
    )

    return ai_service.generate_recommendation(
        equipment_name=equipment_name,
        risk_level=risk_level,
        temperature=payload.temperature,
        vibration=payload.vibration,
        pressure=payload.pressure,
        health_score=health_score,
        failure_probability=failure_probability,
    )
