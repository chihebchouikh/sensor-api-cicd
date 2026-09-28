from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Sensor API", version="1.0.0")


class Reading(BaseModel):
    sensor_id: str
    temperature: float
    humidity: float | None = None


readings: list[dict] = []


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/readings", status_code=201)
def add_reading(reading: Reading):
    entry = reading.model_dump()
    entry["timestamp"] = datetime.now(timezone.utc).isoformat()
    readings.append(entry)
    return entry


@app.get("/readings")
def list_readings(sensor_id: str | None = None):
    if sensor_id:
        return [r for r in readings if r["sensor_id"] == sensor_id]
    return readings

@app.get("/readings/{sensor_id}/stats")
def sensor_stats(sensor_id: str):
    temperatures = [r["temperature"] for r in readings if r["sensor_id"] == sensor_id]

    if not temperatures:
        raise HTTPException(status_code=404, detail="No readings for this sensor")

    return {
        "sensor_id": sensor_id,
        "count": len(temperatures),
        "average": round(sum(temperatures) / len(temperatures), 2),
        "min": min(temperatures),
        "max": max(temperatures),
    }