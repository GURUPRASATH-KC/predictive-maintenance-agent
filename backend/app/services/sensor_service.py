"""
Sensor service — all MongoDB operations for the `sensors` collection.
"""
from datetime import datetime

from app.database import get_database, SENSORS_COLLECTION
from app.schemas.sensor import SensorCreate
from app.utils.helpers import serialize_doc, serialize_list


async def create_sensor_reading(payload: SensorCreate) -> dict:
    db = get_database()
    doc = payload.model_dump()
    doc["timestamp"] = datetime.utcnow()
    result = await db[SENSORS_COLLECTION].insert_one(doc)
    created = await db[SENSORS_COLLECTION].find_one({"_id": result.inserted_id})
    return serialize_doc(created)


async def list_sensor_readings(limit: int = 100) -> list:
    db = get_database()
    cursor = db[SENSORS_COLLECTION].find().sort("timestamp", -1).limit(limit)
    docs = await cursor.to_list(length=limit)
    return serialize_list(docs)


async def list_sensor_readings_for_equipment(equipment_id: str, limit: int = 100) -> list:
    db = get_database()
    cursor = (
        db[SENSORS_COLLECTION]
        .find({"equipment_id": equipment_id})
        .sort("timestamp", -1)
        .limit(limit)
    )
    docs = await cursor.to_list(length=limit)
    return serialize_list(docs)


async def get_latest_reading_for_equipment(equipment_id: str):
    db = get_database()
    doc = await db[SENSORS_COLLECTION].find_one(
        {"equipment_id": equipment_id}, sort=[("timestamp", -1)]
    )
    return serialize_doc(doc) if doc else None
