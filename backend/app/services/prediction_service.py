"""
Prediction service — orchestrates the rule-based health engine and the AI
Maintenance Agent, then persists the result to the `predictions` collection.
"""
from datetime import datetime

from app.database import get_database, PREDICTIONS_COLLECTION
from app.schemas.prediction import PredictionRequest
from app.services import equipment_service, sensor_service, ai_service
from app.utils.health_logic import evaluate_sensor_reading
from app.utils.helpers import serialize_doc, serialize_list


async def run_prediction(payload: PredictionRequest) -> dict:
    equipment = await equipment_service.get_equipment_by_equipment_id(payload.equipment_id)
    equipment_name = equipment["equipment_name"] if equipment else payload.equipment_id

    health_score, risk_level, failure_probability, message = evaluate_sensor_reading(
        payload.temperature,
        payload.vibration,
        payload.pressure,
        equipment_type=equipment["equipment_type"] if equipment else None,
        load=payload.load,
        rpm=payload.rpm,
    )

    ai_recommendation = ai_service.generate_recommendation(
        equipment_name=equipment_name,
        risk_level=risk_level,
        temperature=payload.temperature,
        vibration=payload.vibration,
        pressure=payload.pressure,
        health_score=health_score,
        failure_probability=failure_probability,
        equipment_type=equipment["equipment_type"] if equipment else None,
        load=payload.load,
        rpm=payload.rpm,
    )

    sensor_snapshot = {
        "temperature": payload.temperature,
        "vibration": payload.vibration,
        "pressure": payload.pressure,
        "rpm": payload.rpm,
        "load": payload.load,
    }

    db = get_database()
    doc = {
        "equipment_id": payload.equipment_id,
        "equipment_name": equipment_name,
        "health_score": health_score,
        "risk_level": risk_level,
        "failure_probability": failure_probability,
        "message": message,
        "sensor_snapshot": sensor_snapshot,
        "ai_recommendation": ai_recommendation,
        "created_at": datetime.utcnow(),
    }
    result = await db[PREDICTIONS_COLLECTION].insert_one(doc)
    created = await db[PREDICTIONS_COLLECTION].find_one({"_id": result.inserted_id})

    # Optionally persist the raw sensor reading too, and sync equipment status
    if payload.save_reading:
        from app.schemas.sensor import SensorCreate

        await sensor_service.create_sensor_reading(
            SensorCreate(
                equipment_id=payload.equipment_id,
                temperature=payload.temperature,
                vibration=payload.vibration,
                pressure=payload.pressure,
                rpm=payload.rpm,
                load=payload.load,
            )
        )

    if equipment:
        await equipment_service.update_equipment_status_by_equipment_id(
            payload.equipment_id, risk_level
        )

    return serialize_doc(created)


async def list_predictions(limit: int = 200) -> list:
    db = get_database()
    cursor = db[PREDICTIONS_COLLECTION].find().sort("created_at", -1).limit(limit)
    docs = await cursor.to_list(length=limit)
    return serialize_list(docs)


async def list_predictions_for_equipment(equipment_id: str, limit: int = 100) -> list:
    db = get_database()
    cursor = (
        db[PREDICTIONS_COLLECTION]
        .find({"equipment_id": equipment_id})
        .sort("created_at", -1)
        .limit(limit)
    )
    docs = await cursor.to_list(length=limit)
    return serialize_list(docs)
