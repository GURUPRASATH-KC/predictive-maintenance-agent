"""
Equipment domain model.

This represents the shape of a document as stored in the `equipment`
MongoDB collection. Pydantic schemas (in app/schemas) handle what the API
accepts/returns; this module is the "source of truth" for field names.
"""
from datetime import datetime
from typing import Optional


class EquipmentModel:
    """Plain data holder mirroring the MongoDB document shape."""

    def __init__(
        self,
        equipment_id: str,
        equipment_name: str,
        equipment_type: str,
        location: str,
        installation_date: str,
        status: str = "Normal",
        created_at: Optional[datetime] = None,
    ):
        self.equipment_id = equipment_id
        self.equipment_name = equipment_name
        self.equipment_type = equipment_type
        self.location = location
        self.installation_date = installation_date
        self.status = status
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            "equipment_id": self.equipment_id,
            "equipment_name": self.equipment_name,
            "equipment_type": self.equipment_type,
            "location": self.location,
            "installation_date": self.installation_date,
            "status": self.status,
            "created_at": self.created_at,
        }
