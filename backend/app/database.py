"""
MongoDB Atlas connection handling using Motor (async MongoDB driver).
"""
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings

client: AsyncIOMotorClient | None = None
database = None


def connect_to_mongo():
    """Create the Mongo client and database handle. Call on app startup."""
    global client, database
    client = AsyncIOMotorClient(settings.mongodb_uri)
    database = client[settings.database_name]
    return database


def close_mongo_connection():
    """Close the Mongo client. Call on app shutdown."""
    global client
    if client:
        client.close()


def get_database():
    """Dependency-friendly accessor for the database handle."""
    return database


# Collection name constants so routes/services never hard-code strings
EQUIPMENT_COLLECTION = "equipment"
SENSORS_COLLECTION = "sensors"
PREDICTIONS_COLLECTION = "predictions"
