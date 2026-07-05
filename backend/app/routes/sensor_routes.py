"""
Sensor reading API routes.
"""
from fastapi import APIRouter

from app.schemas.sensor import SensorCreate
from app.services import sensor_service

router = APIRouter(prefix="/api/sensors", tags=["Sensors"])


@router.post("")
async def create_sensor_reading(payload: SensorCreate):
    return await sensor_service.create_sensor_reading(payload)


@router.get("")
async def list_sensor_readings(limit: int = 100):
    return await sensor_service.list_sensor_readings(limit=limit)


@router.get("/equipment/{equipment_id}")
async def list_sensor_readings_for_equipment(equipment_id: str, limit: int = 100):
    return await sensor_service.list_sensor_readings_for_equipment(equipment_id, limit=limit)
