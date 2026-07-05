"""
Dashboard aggregation API routes — power the summary cards, charts, and
recent activity tables on the frontend dashboard.
"""
from fastapi import APIRouter

from app.database import get_database, EQUIPMENT_COLLECTION, PREDICTIONS_COLLECTION
from app.utils.helpers import serialize_list

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/summary")
async def get_summary():
    db = get_database()
    equipment_cursor = db[EQUIPMENT_COLLECTION].find()
    equipment_list = await equipment_cursor.to_list(length=1000)

    total = len(equipment_list)
    normal = sum(1 for e in equipment_list if e.get("status") == "Normal")
    warning = sum(1 for e in equipment_list if e.get("status") == "Warning")
    critical = sum(1 for e in equipment_list if e.get("status") == "Critical")

    total_predictions = await db[PREDICTIONS_COLLECTION].count_documents({})

    return {
        "total_equipment": total,
        "normal_count": normal,
        "warning_count": warning,
        "critical_count": critical,
        "total_predictions": total_predictions,
    }


@router.get("/recent-predictions")
async def get_recent_predictions(limit: int = 10):
    db = get_database()
    cursor = db[PREDICTIONS_COLLECTION].find().sort("created_at", -1).limit(limit)
    docs = await cursor.to_list(length=limit)
    return serialize_list(docs)


@router.get("/risk-distribution")
async def get_risk_distribution():
    db = get_database()
    equipment_cursor = db[EQUIPMENT_COLLECTION].find()
    equipment_list = await equipment_cursor.to_list(length=1000)

    normal = sum(1 for e in equipment_list if e.get("status") == "Normal")
    warning = sum(1 for e in equipment_list if e.get("status") == "Warning")
    critical = sum(1 for e in equipment_list if e.get("status") == "Critical")

    return {
        "labels": ["Normal", "Warning", "Critical"],
        "values": [normal, warning, critical],
    }
