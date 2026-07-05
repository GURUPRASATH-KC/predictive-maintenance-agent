"""
Equipment CRUD API routes.
"""
from fastapi import APIRouter, HTTPException

from app.schemas.equipment import EquipmentCreate, EquipmentUpdate
from app.services import equipment_service

router = APIRouter(prefix="/api/equipment", tags=["Equipment"])


@router.post("")
async def create_equipment(payload: EquipmentCreate):
    existing = await equipment_service.get_equipment_by_equipment_id(payload.equipment_id)
    if existing:
        raise HTTPException(status_code=400, detail="Equipment with this equipment_id already exists")
    return await equipment_service.create_equipment(payload)


@router.get("")
async def list_equipment():
    return await equipment_service.list_equipment()


@router.get("/{id}")
async def get_equipment(id: str):
    doc = await equipment_service.get_equipment_by_mongo_id(id)
    if not doc:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return doc


@router.put("/{id}")
async def update_equipment(id: str, payload: EquipmentUpdate):
    doc = await equipment_service.update_equipment(id, payload)
    if not doc:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return doc


@router.delete("/{id}")
async def delete_equipment(id: str):
    deleted = await equipment_service.delete_equipment(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return {"success": True, "message": "Equipment deleted"}
