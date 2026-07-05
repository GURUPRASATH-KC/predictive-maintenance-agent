"""
Prediction result domain model — mirrors the `predictions` MongoDB collection.
"""
from datetime import datetime
from typing import Optional


class PredictionModel:
    def __init__(
        self,
        equipment_id: str,
        equipment_name: str,
        health_score: float,
        risk_level: str,
        failure_probability: float,
        message: str,
        sensor_snapshot: dict,
        ai_recommendation: Optional[dict] = None,
        created_at: Optional[datetime] = None,
    ):
        self.equipment_id = equipment_id
        self.equipment_name = equipment_name
        self.health_score = health_score
        self.risk_level = risk_level
        self.failure_probability = failure_probability
        self.message = message
        self.sensor_snapshot = sensor_snapshot
        self.ai_recommendation = ai_recommendation
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            "equipment_id": self.equipment_id,
            "equipment_name": self.equipment_name,
            "health_score": self.health_score,
            "risk_level": self.risk_level,
            "failure_probability": self.failure_probability,
            "message": self.message,
            "sensor_snapshot": self.sensor_snapshot,
            "ai_recommendation": self.ai_recommendation,
            "created_at": self.created_at,
        }
