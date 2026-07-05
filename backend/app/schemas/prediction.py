"""
Pydantic schemas for prediction API requests/responses.
"""
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    equipment_id: str = Field(..., examples=["EQ001"])
    # Validation to prevent obviously fake sensor inputs
    temperature: float = Field(..., ge=-40.0, le=200.0, examples=[88.0])
    vibration: float = Field(..., ge=0.0, le=50.0, examples=[8.1])
    pressure: float = Field(..., ge=0.0, le=500.0, examples=[135.0])
    rpm: Optional[float] = Field(default=None, ge=0.0, le=10000.0, examples=[1600])
    load: Optional[float] = Field(default=None, ge=0.0, le=100.0, examples=[90])
    save_reading: bool = Field(
        default=True,
        description="If true, also stores this sensor reading in the sensors collection.",
    )


class AIRecommendation(BaseModel):
    possible_issue: str
    reason: str
    recommended_action: List[str]
    urgency: str
    inspection_window: str


class PredictionResponse(BaseModel):
    id: Optional[str] = None
    equipment_id: str
    equipment_name: Optional[str] = None
    health_score: float
    risk_level: str
    failure_probability: float
    message: str
    ai_recommendation: Optional[AIRecommendation] = None
    created_at: Optional[datetime] = None
