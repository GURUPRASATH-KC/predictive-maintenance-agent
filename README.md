# AI-Based Predictive Maintenance Agent for Power System Equipment

A full-stack AI-assisted dashboard for monitoring and predicting failures in critical electrical power-system assets such as transformers, circuit breakers, generators, induction motors, switchgear panels, and capacitor banks. Built as a clean, beginner-friendly final-year / placement mini-project with a strong EEE/power systems focus.

---

## Overview

The system lets you:

1. Register and manage power-system equipment such as transformers, breakers, generators, motors, switchgear, and capacitor banks.
2. Record sensor readings for each asset using a shared predictive sensor model adapted for electrical equipment.
3. Run a **prediction** that classifies equipment as **Normal / Warning / Critical**, with a health score (0–100) and failure probability (%).
4. Get an **AI Maintenance Agent** recommendation with issue diagnosis, recommended actions, urgency, and inspection timing.
5. View everything on a professional dashboard with charts, tables, and prediction history.

The prediction logic is a transparent, rule-based engine (not a black-box ML model), so it remains easy to explain in an interview, presentation, or demo.

---

## Features

- **Equipment Management** — full CRUD for electrical assets.
- **Sensor Data** — manual sensor logging with power-system-oriented example values.
- **Prediction Engine** — equipment-specific threshold-based health scoring, explainable and tunable.
- **AI Maintenance Agent** — diagnosis, likely cause, action list, urgency, inspection window. Works with or without an LLM key.
- **Dashboard** — summary cards, health distribution chart, recent predictions, asset health overview.
- **Prediction History** — filterable log of every prediction ever run.
- **Sample/seed data** — six realistic power-system demo assets with mixed Normal/Warning/Critical conditions.

---

## Tech Stack

**Backend:** Python, FastAPI, Motor (async MongoDB driver)
**Database:** MongoDB Atlas
**Frontend:** React + Vite, Tailwind CSS, Axios, React Router, Recharts, Lucide icons

---

## Folder Structure

```
predictive-maintenance-agent/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app entrypoint
│   │   ├── config.py               # Settings loaded from .env
│   │   ├── database.py             # MongoDB connection
│   │   ├── models/                 # Domain models (document shape)
│   │   │   ├── equipment.py
│   │   │   ├── sensor.py
│   │   │   └── prediction.py
│   │   ├── schemas/                # Pydantic request/response schemas
│   │   │   ├── equipment.py
│   │   │   ├── sensor.py
│   │   │   └── prediction.py
│   │   ├── routes/                 # API route definitions
│   │   │   ├── equipment_routes.py
│   │   │   ├── sensor_routes.py
│   │   │   ├── prediction_routes.py
│   │   │   ├── dashboard_routes.py
│   │   │   └── ai_routes.py
│   │   ├── services/               # Business logic + DB access
│   │   │   ├── equipment_service.py
│   │   │   ├── sensor_service.py
│   │   │   ├── prediction_service.py
│   │   │   └── ai_service.py       # AI Maintenance Agent (rule-based + optional LLM)
│   │   └── utils/
│   │       ├── health_logic.py     # Threshold rules, health score, failure %
│   │       └── helpers.py
│   ├── seed_data.py                # Populates sample equipment/sensors/predictions
│   ├── requirements.txt
│   └── .env.example
│
└── frontend/
    ├── src/
    │   ├── pages/                  # Dashboard, Equipment, Sensors, Predict, History, Recommendations
    │   ├── layout/                 # Sidebar, Navbar
    │   ├── components/             # StatCard, RiskBadge, AIRecommendationCard, States
    │   ├── api/                    # Axios API client + per-resource functions
    │   ├── App.jsx
    │   └── main.jsx
    ├── package.json
    ├── tailwind.config.js
    └── .env.example
```

---

## How Prediction Works

- The app evaluates temperature, vibration, pressure, and optional load/rpm values against equipment-specific thresholds.
- Each metric contributes to a 0–100 health score. Lower scores imply higher failure probability.
- Risk is classified as Normal, Warning, or Critical based on the asset type (transformer, breaker, generator, motor, switchgear, or capacitor bank).
- Recommendations are generated using a deterministic, explainable rule-based engine and can optionally use an OpenAI model if configured.

## Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- A free [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register) cluster (or a local MongoDB instance)

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# then edit .env and paste your MongoDB Atlas connection string into MONGODB_URI
```

Populate sample data (recommended so the dashboard isn't empty on first run):

```bash
python seed_data.py
```

Run the API:

```bash
uvicorn app.main:app --reload --port 8000
```

The API is now live at `http://localhost:8000`. Interactive docs: `http://localhost:8000/docs`.

### 2. Frontend

```bash
cd frontend
npm install
cp .env.example .env   # points the frontend at http://localhost:8000 by default
npm run dev
```

Open `http://localhost:5173` in your browser.

---

## Environment Variables

### backend/.env

| Variable | Description |
|---|---|
| `MONGODB_URI` | Your MongoDB Atlas connection string |
| `DATABASE_NAME` | Database name (default: `predictive_maintenance`) |
| `OPENAI_API_KEY` | Optional. If set, AI recommendations use OpenAI. If empty, the rule-based generator is used automatically. |
| `FRONTEND_ORIGIN` | Frontend URL allowed by CORS (default: `http://localhost:5173`) |

### frontend/.env

| Variable | Description |
|---|---|
| `VITE_API_BASE_URL` | Backend API base URL (default: `http://localhost:8000`) |

---

## API Reference

### Equipment
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/equipment` | Create equipment |
| GET | `/api/equipment` | List all equipment |
| GET | `/api/equipment/{id}` | Get one equipment (Mongo `_id`) |
| PUT | `/api/equipment/{id}` | Update equipment |
| DELETE | `/api/equipment/{id}` | Delete equipment |

### Sensors
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/sensors` | Add a sensor reading |
| GET | `/api/sensors` | List recent readings (all equipment) |
| GET | `/api/sensors/equipment/{equipment_id}` | Readings for one equipment |

### Prediction
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/predict` | Run a prediction from sensor values |
| GET | `/api/predictions` | List all past predictions |
| GET | `/api/predictions/{equipment_id}` | Predictions for one equipment |

### Dashboard
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/dashboard/summary` | Counts by risk level |
| GET | `/api/dashboard/recent-predictions` | Latest N predictions |
| GET | `/api/dashboard/risk-distribution` | Data for the pie chart |

### AI
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/ai/recommendation` | Get a standalone AI maintenance recommendation |

---

## Sample API Responses

**POST `/api/predict`**
```json
{
  "id": "665f1a2b3c4d5e6f7a8b9c0d",
  "equipment_id": "EQ003",
  "equipment_name": "Compressor C",
  "health_score": 22.4,
  "risk_level": "Critical",
  "failure_probability": 77.6,
  "message": "High chance of failure due to elevated temperature and abnormal vibration and irregular pressure exceeding safe thresholds.",
  "ai_recommendation": {
    "equipment": "Compressor C",
    "risk_level": "Critical",
    "possible_issue": "Bearing wear or rotor imbalance",
    "reason": "Vibration exceeds the normal threshold and temperature is above the safe operating range.",
    "recommended_action": [
      "Inspect bearings",
      "Check shaft/motor alignment",
      "Inspect cooling system / fans",
      "Check lubrication levels"
    ],
    "urgency": "High",
    "inspection_window": "Within 24 hours"
  },
  "created_at": "2026-07-05T10:30:00Z"
}
```

**GET `/api/dashboard/summary`**
```json
{
  "total_equipment": 4,
  "normal_count": 1,
  "warning_count": 2,
  "critical_count": 1,
  "total_predictions": 4
}
```

---

## Prediction Logic (thresholds)

| Condition | Normal | Warning | Critical |
|---|---|---|---|
| Temperature (°C) | < 70 | 70–85 | > 85 |
| Vibration (mm/s) | < 4 | 4–7 | > 7 |
| Pressure | 80–120 | 60–140 | outside 60–140 |

The health score is a weighted average of per-metric sub-scores (vibration weighted highest, since it's typically the strongest early indicator of mechanical failure), and failure probability is derived directly from the health score. All thresholds live in `backend/app/utils/health_logic.py` and can be tuned freely.

## How prediction works

- The app evaluates `temperature`, `vibration`, and `pressure` against tunable thresholds in `backend/app/utils/health_logic.py`.
- Each metric produces a 0–100 sub-score (100 = ideal). Vibration is weighted highest, then temperature, then pressure.
- The overall health score is a weighted average of the sub-scores and is shown as a value out of 100.
- Failure probability is a simple inverse of the health score (lower health → higher probability).
- Risk levels are classified as `Normal`, `Warning`, or `Critical` using the same thresholds; recommendations are then produced by a deterministic rule-based generator (with an optional OpenAI-backed generator when an API key is provided).

This keeps the predictions explainable and easy to demonstrate during a project walkthrough.

---

## Future Enhancements

- Add live sensor streaming or IoT device integration.
- Add role-based authentication for plant operators.
- Add more detailed asset-specific analytics and trend graphs.
- Add email or SMS alerts for Critical equipment conditions.
