"""
Predictive Maintenance Agent — FastAPI application entrypoint.

Run locally with:
    uvicorn app.main:app --reload --port 8000
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import connect_to_mongo, close_mongo_connection
from app.routes import (
    equipment_routes,
    sensor_routes,
    prediction_routes,
    dashboard_routes,
    ai_routes,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_to_mongo()
    yield
    close_mongo_connection()


app = FastAPI(
    title="Predictive Maintenance Agent API",
    description="Backend for the Predictive Maintenance AI Agent project.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(equipment_routes.router)
app.include_router(sensor_routes.router)
app.include_router(prediction_routes.router)
app.include_router(prediction_routes.history_router)
app.include_router(dashboard_routes.router)
app.include_router(ai_routes.router)


@app.get("/")
async def root():
    return {"message": "Predictive Maintenance Agent API is running", "docs": "/docs"}


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
