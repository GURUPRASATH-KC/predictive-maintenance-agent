"""
Equipment service — all MongoDB operations for the `equipment` collection.
"""
from datetime import datetime
from typing import Optional

from bson import ObjectId
from bson.errors import InvalidId

from app.database import get_database, EQUIPMENT_COLLECTION
from app.schemas.equipment import EquipmentCreate, EquipmentUpdate
from app.utils.helpers import serialize_doc, serialize_list


async def create_equipment(payload: EquipmentCreate) -> dict:
    db = get_database()
    doc = payload.model_dump()
    doc["status"] = doc.get("status") or "Normal"
    doc["created_at"] = datetime.utcnow()
    result = await db[EQUIPMENT_COLLECTION].insert_one(doc)
    created = await db[EQUIPMENT_COLLECTION].find_one({"_id": result.inserted_id})
    return serialize_doc(created)


async def list_equipment() -> list:
    db = get_database()
    cursor = db[EQUIPMENT_COLLECTION].find().sort("created_at", -1)
    docs = await cursor.to_list(length=1000)
    return serialize_list(docs)


async def get_equipment_by_mongo_id(id: str) -> Optional[dict]:
    db = get_database()
    try:
        oid = ObjectId(id)
    except InvalidId:
        return None
    doc = await db[EQUIPMENT_COLLECTION].find_one({"_id": oid})
    return serialize_doc(doc) if doc else None


async def get_equipment_by_equipment_id(equipment_id: str) -> Optional[dict]:
    db = get_database()
    doc = await db[EQUIPMENT_COLLECTION].find_one({"equipment_id": equipment_id})
    return serialize_doc(doc) if doc else None


async def update_equipment(id: str, payload: EquipmentUpdate) -> Optional[dict]:
    db = get_database()
    try:
        oid = ObjectId(id)
    except InvalidId:
        return None

    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
    if not update_data:
        return await get_equipment_by_mongo_id(id)

    await db[EQUIPMENT_COLLECTION].update_one({"_id": oid}, {"$set": update_data})
    doc = await db[EQUIPMENT_COLLECTION].find_one({"_id": oid})
    return serialize_doc(doc) if doc else None


async def delete_equipment(id: str) -> bool:
    db = get_database()
    try:
        oid = ObjectId(id)
    except InvalidId:
        return False
    result = await db[EQUIPMENT_COLLECTION].delete_one({"_id": oid})
    return result.deleted_count > 0


async def update_equipment_status_by_equipment_id(equipment_id: str, status: str) -> None:
    """Used by the prediction service to keep equipment.status in sync with the latest risk level."""
    db = get_database()
    await db[EQUIPMENT_COLLECTION].update_one(
        {"equipment_id": equipment_id}, {"$set": {"status": status}}
    )
