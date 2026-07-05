"""
Pydantic schemas for sensor reading API requests/responses.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SensorCreate(BaseModel):
    equipment_id: str = Field(..., examples=["EQ001"])
    # Reasonable industrial ranges to prevent absurd inputs
    temperature: float = Field(..., ge=-40.0, le=200.0, examples=[78.5])
    vibration: float = Field(..., ge=0.0, le=50.0, examples=[5.2])
    pressure: float = Field(..., ge=0.0, le=500.0, examples=[102.0])
    rpm: Optional[float] = Field(default=None, ge=0.0, le=10000.0, examples=[1450])
    load: Optional[float] = Field(default=None, ge=0.0, le=100.0, examples=[65])


class SensorResponse(BaseModel):
    id: str
    equipment_id: str
    temperature: float
    vibration: float
    pressure: float
    rpm: Optional[float] = None
    load: Optional[float] = None
    timestamp: datetime
