"""
Rule-based health scoring and risk classification for power-system assets.

The logic remains explainable and lightweight while adapting to the equipment
context so the project feels relevant for EEE/power systems.
"""
from typing import Optional, Tuple

# Default thresholds used as a fallback.
TEMP_NORMAL_MAX = 70.0
TEMP_WARNING_MAX = 85.0
VIBRATION_NORMAL_MAX = 4.0
VIBRATION_WARNING_MAX = 7.0
PRESSURE_NORMAL_RANGE = (80.0, 120.0)
PRESSURE_WARNING_RANGE = (60.0, 140.0)

EQUIPMENT_RULES = {
    "Transformer": {
        "temp": {"normal": 70.0, "warning": 85.0, "critical": 95.0},
        "vibration": {"normal": 1.5, "warning": 2.5, "critical": 4.0},
        "pressure": {"normal": (85.0, 110.0), "warning": (75.0, 120.0)},
        "load": {"warning": 80.0, "critical": 92.0},
    },
    "Breaker": {
        "temp": {"normal": 55.0, "warning": 70.0, "critical": 85.0},
        "vibration": {"normal": 1.0, "warning": 1.8, "critical": 2.5},
        "pressure": {"normal": (85.0, 115.0), "warning": (80.0, 120.0)},
        "load": {"warning": 65.0, "critical": 80.0},
    },
    "Generator": {
        "temp": {"normal": 75.0, "warning": 90.0, "critical": 105.0},
        "vibration": {"normal": 2.5, "warning": 4.5, "critical": 6.0},
        "pressure": {"normal": (80.0, 115.0), "warning": (70.0, 130.0)},
        "load": {"warning": 80.0, "critical": 92.0},
    },
    "Motor": {
        "temp": {"normal": 70.0, "warning": 85.0, "critical": 95.0},
        "vibration": {"normal": 2.5, "warning": 4.5, "critical": 6.5},
        "pressure": {"normal": (85.0, 115.0), "warning": (75.0, 125.0)},
        "load": {"warning": 80.0, "critical": 92.0},
    },
    "Switchgear": {
        "temp": {"normal": 60.0, "warning": 75.0, "critical": 90.0},
        "vibration": {"normal": 0.8, "warning": 1.3, "critical": 2.0},
        "pressure": {"normal": (85.0, 110.0), "warning": (80.0, 115.0)},
        "load": {"warning": 75.0, "critical": 90.0},
    },
    "Capacitor Bank": {
        "temp": {"normal": 58.0, "warning": 72.0, "critical": 85.0},
        "vibration": {"normal": 0.6, "warning": 1.0, "critical": 1.5},
        "pressure": {"normal": (85.0, 115.0), "warning": (80.0, 120.0)},
        "load": {"warning": 75.0, "critical": 90.0},
    },
}


def _normalize_equipment_type(equipment_type: Optional[str]) -> str:
    if not equipment_type:
        return "Transformer"
    mapping = {
        "power transformer": "Transformer",
        "transformer": "Transformer",
        "breaker": "Breaker",
        "circuit breaker": "Breaker",
        "generator": "Generator",
        "motor": "Motor",
        "induction motor": "Motor",
        "switchgear": "Switchgear",
        "switchgear panel": "Switchgear",
        "capacitor bank": "Capacitor Bank",
        "capacitor": "Capacitor Bank",
    }
    return mapping.get(equipment_type.lower(), equipment_type)


def _get_rules(equipment_type: Optional[str]) -> dict:
    return EQUIPMENT_RULES.get(_normalize_equipment_type(equipment_type), EQUIPMENT_RULES["Transformer"])


def _score_temperature(temperature: float, equipment_type: Optional[str]) -> float:
    rules = _get_rules(equipment_type)["temp"]
    if temperature <= rules["normal"]:
        return 100.0
    if temperature <= rules["warning"]:
        span = rules["warning"] - rules["normal"]
        progress = (temperature - rules["normal"]) / span
        return 100.0 - (progress * 40.0)
    overshoot = min(temperature - rules["warning"], 40.0)
    return max(60.0 - (overshoot / 40.0) * 60.0, 0.0)


def _score_vibration(vibration: float, equipment_type: Optional[str]) -> float:
    rules = _get_rules(equipment_type)["vibration"]
    if vibration <= rules["normal"]:
        return 100.0
    if vibration <= rules["warning"]:
        span = rules["warning"] - rules["normal"]
        progress = (vibration - rules["normal"]) / span
        return 100.0 - (progress * 40.0)
    overshoot = min(vibration - rules["warning"], 6.0)
    return max(60.0 - (overshoot / 6.0) * 60.0, 0.0)


def _score_pressure(pressure: float, equipment_type: Optional[str]) -> float:
    rules = _get_rules(equipment_type)["pressure"]
    low_n, high_n = rules["normal"]
    low_w, high_w = rules["warning"]

    if low_n <= pressure <= high_n:
        return 100.0
    if low_w <= pressure < low_n:
        progress = (low_n - pressure) / (low_n - low_w)
        return 100.0 - (progress * 40.0)
    if high_n < pressure <= high_w:
        progress = (pressure - high_n) / (high_w - high_n)
        return 100.0 - (progress * 40.0)

    if pressure < low_w:
        overshoot = min(low_w - pressure, 40.0)
    else:
        overshoot = min(pressure - high_w, 40.0)
    return max(60.0 - (overshoot / 40.0) * 60.0, 0.0)


def _score_load(load: Optional[float], equipment_type: Optional[str]) -> float:
    if load is None:
        return 100.0
    rules = _get_rules(equipment_type)["load"]
    if load <= rules["warning"]:
        return 100.0
    if load <= rules["critical"]:
        progress = (load - rules["warning"]) / (rules["critical"] - rules["warning"])
        return 100.0 - (progress * 35.0)
    return max(65.0 - ((load - rules["critical"]) / 10.0) * 65.0, 0.0)


def _score_rpm(rpm: Optional[float], equipment_type: Optional[str]) -> float:
    if equipment_type not in {"Motor", "Induction Motor"} or rpm is None:
        return 100.0
    if 1200 <= rpm <= 1800:
        return 100.0
    if 900 <= rpm < 1200:
        return 85.0
    return max(60.0 - (abs(rpm - 1400) / 200.0) * 25.0, 0.0)


def classify_risk(
    temperature: float,
    vibration: float,
    pressure: float,
    equipment_type: Optional[str] = None,
    load: Optional[float] = None,
    rpm: Optional[float] = None,
) -> str:
    rules = _get_rules(equipment_type)
    temp_warning = rules["temp"]["warning"]
    temp_critical = rules["temp"]["critical"]
    vib_warning = rules["vibration"]["warning"]
    vib_critical = rules["vibration"]["critical"]
    low_n, high_n = rules["pressure"]["normal"]
    low_w, high_w = rules["pressure"]["warning"]
    load_warning = rules["load"]["warning"]
    load_critical = rules["load"]["critical"]

    critical = (
        temperature > temp_critical
        or vibration > vib_critical
        or not (low_w <= pressure <= high_w)
        or (load is not None and load > load_critical)
        or (equipment_type in {"Motor", "Induction Motor"} and rpm is not None and rpm < 900)
    )
    if critical:
        return "Critical"

    warning = (
        temperature > temp_warning
        or vibration > vib_warning
        or not (low_n <= pressure <= high_n)
        or (load is not None and load > load_warning)
        or (equipment_type in {"Motor", "Induction Motor"} and rpm is not None and rpm < 1000)
    )
    if warning:
        return "Warning"

    return "Normal"


def calculate_health_score(
    temperature: float,
    vibration: float,
    pressure: float,
    equipment_type: Optional[str] = None,
    load: Optional[float] = None,
    rpm: Optional[float] = None,
) -> float:
    temp_score = _score_temperature(temperature, equipment_type)
    vib_score = _score_vibration(vibration, equipment_type)
    pressure_score = _score_pressure(pressure, equipment_type)
    load_score = _score_load(load, equipment_type)
    rpm_score = _score_rpm(rpm, equipment_type)

    if equipment_type in {"Motor", "Induction Motor"}:
        weighted = (temp_score * 0.25) + (vib_score * 0.25) + (pressure_score * 0.2) + (load_score * 0.2) + (rpm_score * 0.1)
    else:
        weighted = (temp_score * 0.3) + (vib_score * 0.3) + (pressure_score * 0.2) + (load_score * 0.2)
    return round(weighted, 1)


def calculate_failure_probability(health_score: float) -> float:
    probability = 100.0 - health_score
    probability = probability * 0.95
    return round(min(max(probability, 0.0), 99.0), 1)


def generate_message(
    risk_level: str,
    temperature: float,
    vibration: float,
    pressure: float,
    equipment_type: Optional[str] = None,
    load: Optional[float] = None,
) -> str:
    equipment = _normalize_equipment_type(equipment_type)
    issues = []
    if temperature > TEMP_NORMAL_MAX:
        issues.append("elevated temperature")
    if vibration > VIBRATION_NORMAL_MAX:
        issues.append("abnormal vibration")
    if not (PRESSURE_NORMAL_RANGE[0] <= pressure <= PRESSURE_NORMAL_RANGE[1]):
        issues.append("pressure abnormality")
    if load is not None and load > 75:
        issues.append("load stress")

    if risk_level == "Normal":
        return f"{equipment} readings are within normal operating limits."

    issue_text = " and ".join(issues) if issues else "one or more abnormal electrical parameters"
    if equipment == "Transformer":
        diagnosis = "Elevated transformer temperature and loading indicate insulation stress and possible cooling inefficiency."
    elif equipment == "Breaker":
        diagnosis = "Contact heating and pressure irregularity suggest breaker mechanism stress or contact wear."
    elif equipment == "Generator":
        diagnosis = "High generator vibration and temperature suggest bearing wear or rotor imbalance."
    elif equipment == "Motor":
        diagnosis = "Motor overheating and vibration indicate possible bearing wear or misalignment."
    elif equipment == "Switchgear":
        diagnosis = "Rising hotspot temperature and overload indicate switchgear insulation or joint stress."
    else:
        diagnosis = "The asset is showing abnormal electrical stress and should be inspected promptly."

    if risk_level == "Warning":
        return f"{diagnosis} Monitor the {equipment.lower()} closely."
    return f"{diagnosis} Immediate inspection is recommended."


def evaluate_sensor_reading(
    temperature: float,
    vibration: float,
    pressure: float,
    equipment_type: Optional[str] = None,
    load: Optional[float] = None,
    rpm: Optional[float] = None,
) -> Tuple[float, str, float, str]:
    """Convenience wrapper returning (health_score, risk_level, failure_probability, message)."""
    risk_level = classify_risk(temperature, vibration, pressure, equipment_type, load, rpm)
    health_score = calculate_health_score(temperature, vibration, pressure, equipment_type, load, rpm)
    failure_probability = calculate_failure_probability(health_score)
    message = generate_message(risk_level, temperature, vibration, pressure, equipment_type, load)
    return health_score, risk_level, failure_probability, message
