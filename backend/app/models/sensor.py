"""
Sensor reading domain model — mirrors the `sensors` MongoDB collection.
"""
from datetime import datetime
from typing import Optional


class SensorModel:
    def __init__(
        self,
        equipment_id: str,
        temperature: float,
        vibration: float,
        pressure: float,
        rpm: Optional[float] = None,
        load: Optional[float] = None,
        timestamp: Optional[datetime] = None,
    ):
        self.equipment_id = equipment_id
        self.temperature = temperature
        self.vibration = vibration
        self.pressure = pressure
        self.rpm = rpm
        self.load = load
        self.timestamp = timestamp or datetime.utcnow()

    def to_dict(self):
        return {
            "equipment_id": self.equipment_id,
            "temperature": self.temperature,
            "vibration": self.vibration,
            "pressure": self.pressure,
            "rpm": self.rpm,
            "load": self.load,
            "timestamp": self.timestamp,
        }
