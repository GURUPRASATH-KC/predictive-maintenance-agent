"""
Pydantic schemas for equipment API requests/responses.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class EquipmentCreate(BaseModel):
    equipment_id: str = Field(..., examples=["EQ001"])
    equipment_name: str = Field(..., examples=["Motor A"])
    equipment_type: str = Field(..., examples=["Motor"])
    location: str = Field(..., examples=["Plant Floor 1"])
    installation_date: str = Field(..., examples=["2023-01-15"])
    status: Optional[str] = Field(default="Normal", examples=["Normal"])


class EquipmentUpdate(BaseModel):
    equipment_name: Optional[str] = None
    equipment_type: Optional[str] = None
    location: Optional[str] = None
    installation_date: Optional[str] = None
    status: Optional[str] = None


class EquipmentResponse(BaseModel):
    id: str
    equipment_id: str
    equipment_name: str
    equipment_type: str
    location: str
    installation_date: str
    status: str
    created_at: datetime
