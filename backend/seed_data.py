"""
Seed script for the power-system predictive maintenance demo.
"""
import asyncio
import random
from datetime import datetime, timedelta

from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings
from app.services import ai_service
from app.utils.health_logic import evaluate_sensor_reading

EQUIPMENT = [
    {
        "equipment_id": "TR001",
        "equipment_name": "Power Transformer T1",
        "equipment_type": "Transformer",
        "location": "Substation A",
        "installation_date": "2019-04-12",
    },
    {
        "equipment_id": "CB001",
        "equipment_name": "Circuit Breaker CB-101",
        "equipment_type": "Breaker",
        "location": "Switchyard A",
        "installation_date": "2021-08-02",
    },
    {
        "equipment_id": "GEN001",
        "equipment_name": "Generator G1",
        "equipment_type": "Generator",
        "location": "Plant Section A",
        "installation_date": "2017-11-18",
    },
    {
        "equipment_id": "MOT001",
        "equipment_name": "Induction Motor M1",
        "equipment_type": "Motor",
        "location": "Pump House",
        "installation_date": "2020-05-20",
    },
    {
        "equipment_id": "SWG001",
        "equipment_name": "Switchgear Panel SG-1",
        "equipment_type": "Switchgear",
        "location": "Control Room",
        "installation_date": "2022-01-10",
    },
    {
        "equipment_id": "CAP001",
        "equipment_name": "Capacitor Bank C1",
        "equipment_type": "Capacitor Bank",
        "location": "Substation B",
        "installation_date": "2023-03-05",
    },
]

TYPE_RANGES = {
    "Transformer": {
        "temperature": (55.0, 95.0),
        "vibration": (0.5, 4.0),
        "pressure": (70.0, 120.0),
        "load": (40, 95),
    },
    "Breaker": {
        "temperature": (30.0, 85.0),
        "vibration": (0.0, 2.5),
        "pressure": (80.0, 120.0),
        "load": (20, 80),
    },
    "Generator": {
        "temperature": (50.0, 110.0),
        "vibration": (1.0, 8.0),
        "pressure": (70.0, 130.0),
        "load": (35, 100),
    },
    "Motor": {
        "temperature": (40.0, 95.0),
        "vibration": (1.0, 8.0),
        "pressure": (80.0, 125.0),
        "rpm": (900, 1800),
        "load": (30, 100),
    },
    "Switchgear": {
        "temperature": (35.0, 90.0),
        "vibration": (0.0, 2.0),
        "pressure": (80.0, 115.0),
        "load": (25, 95),
    },
    "Capacitor Bank": {
        "temperature": (35.0, 85.0),
        "vibration": (0.0, 1.5),
        "pressure": (85.0, 120.0),
        "load": (20, 100),
    },
}


def _sample_within(rng):
    return round(random.uniform(rng[0], rng[1]), 1)


def generate_reading(equipment_type: str, severity: str = "normal"):
    base = TYPE_RANGES.get(equipment_type, TYPE_RANGES["Transformer"])
    temp = _sample_within(base["temperature"])
    vib = _sample_within(base["vibration"])
    pres = _sample_within(base["pressure"])
    load = int(_sample_within(base["load"]))
    reading = {
        "temperature": round(temp, 1),
        "vibration": round(vib, 2),
        "pressure": round(pres, 1),
        "load": load,
    }
    if equipment_type == "Motor":
        reading["rpm"] = int(_sample_within(base["rpm"]))

    if severity == "warning":
        reading["temperature"] += random.uniform(5.0, 12.0)
        reading["vibration"] += random.uniform(0.8, 1.5)
        reading["pressure"] += random.uniform(3.0, 8.0)
        reading["load"] = min(100, reading["load"] + random.randint(5, 12))
    elif severity == "critical":
        reading["temperature"] += random.uniform(12.0, 25.0)
        reading["vibration"] += random.uniform(1.5, 3.5)
        reading["pressure"] += random.uniform(8.0, 20.0)
        reading["load"] = min(100, reading["load"] + random.randint(12, 25))

    reading["temperature"] = round(reading["temperature"], 1)
    reading["vibration"] = round(reading["vibration"], 2)
    reading["pressure"] = round(reading["pressure"], 1)
    return reading


async def seed():
    client = AsyncIOMotorClient(settings.mongodb_uri)
    db = client[settings.database_name]

    print("Clearing existing data...")
    await db.equipment.delete_many({})
    await db.sensors.delete_many({})
    await db.predictions.delete_many({})

    print("Inserting equipment...")
    for eq in EQUIPMENT:
        await db.equipment.insert_one({**eq, "status": "Normal", "created_at": datetime.utcnow()})

    print("Inserting sensor readings and predictions...")
    desired_severity = {
        "TR001": "warning",
        "CB001": "normal",
        "GEN001": "critical",
        "MOT001": "normal",
        "SWG001": "warning",
        "CAP001": "critical",
    }

    for eq in EQUIPMENT:
        equipment_id = eq["equipment_id"]
        equipment_type = eq["equipment_type"]
        severity = desired_severity.get(equipment_id, "normal")
        readings = []
        for hours_ago, sev in [(24, "normal"), (6, severity), (1, severity)]:
            reading = generate_reading(equipment_type, severity=sev)
            sensor_doc = {
                "equipment_id": equipment_id,
                **reading,
                "timestamp": datetime.utcnow() - timedelta(hours=hours_ago),
            }
            await db.sensors.insert_one(sensor_doc)
            readings.append(reading)

        latest_reading = readings[-1]
        health_score, risk_level, failure_probability, message = evaluate_sensor_reading(
            latest_reading["temperature"],
            latest_reading["vibration"],
            latest_reading["pressure"],
            equipment_type=equipment_type,
            load=latest_reading.get("load"),
            rpm=latest_reading.get("rpm"),
        )
        ai_rec = ai_service.generate_recommendation(
            equipment_name=eq["equipment_name"],
            risk_level=risk_level,
            temperature=latest_reading["temperature"],
            vibration=latest_reading["vibration"],
            pressure=latest_reading["pressure"],
            health_score=health_score,
            failure_probability=failure_probability,
            equipment_type=equipment_type,
            load=latest_reading.get("load"),
            rpm=latest_reading.get("rpm"),
        )
        await db.predictions.insert_one({
            "equipment_id": equipment_id,
            "equipment_name": eq["equipment_name"],
            "health_score": health_score,
            "risk_level": risk_level,
            "failure_probability": failure_probability,
            "message": message,
            "sensor_snapshot": latest_reading,
            "ai_recommendation": ai_rec,
            "created_at": datetime.utcnow(),
        })
        await db.equipment.update_one({"equipment_id": equipment_id}, {"$set": {"status": risk_level}})

    print("Seed complete! Sample data:")
    for eq in EQUIPMENT:
        latest = await db.predictions.find_one({"equipment_id": eq["equipment_id"]}, sort=[("created_at", -1)])
        status = latest.get("risk_level") if latest else "Unknown"
        print(f"  {eq['equipment_id']} - {eq['equipment_name']}: {status}")

    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
