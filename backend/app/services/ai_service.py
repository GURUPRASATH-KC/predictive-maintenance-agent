"""
AI Maintenance Agent for power-system equipment.

The rule-based generator remains available without an API key, but the
recommendations now describe electrical asset issues and actions.
"""
import json
from typing import Optional

from app.config import settings
from app.utils.health_logic import _normalize_equipment_type

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - openai is optional
    OpenAI = None


def _rule_based_recommendation(
    equipment_name: str,
    risk_level: str,
    temperature: float,
    vibration: float,
    pressure: float,
    equipment_type: Optional[str] = None,
    health_score: Optional[float] = None,
    failure_probability: Optional[float] = None,
) -> dict:
    equipment_type = _normalize_equipment_type(equipment_type)
    actions = []
    causes = []

    high_temp = temperature > 75
    high_vibration = vibration > 2.5
    abnormal_pressure = not (80 <= pressure <= 120)

    if equipment_type == "Transformer":
        if high_temp:
            causes.append("oil/winding temperature is elevated")
            actions.extend([
                "Inspect cooling fans and radiator operation",
                "Check transformer oil level and oil quality",
                "Perform DGA if overheating persists",
            ])
        if abnormal_pressure:
            causes.append("oil/gas pressure is outside the normal band")
            actions.append("Inspect bushings and cooling circuit")
        if high_vibration:
            causes.append("core or winding vibration is abnormal")
            actions.append("Inspect internal insulation and mechanical mounting")
        if not actions:
            actions.append("Continue routine thermal and oil monitoring")
        possible_issue = "Transformer overheating or insulation stress"
        reason = "Temperature, pressure, and vibration values indicate possible insulation stress or cooling inefficiency."
    elif equipment_type == "Breaker":
        if high_temp:
            causes.append("contact temperature is high")
            actions.extend([
                "Inspect breaker contacts for wear and heating",
                "Verify trip/close mechanism operation",
                "Measure contact resistance",
            ])
        if abnormal_pressure:
            causes.append("SF6 or air pressure is abnormal")
            actions.append("Check pressure level and leakage points")
        if high_vibration:
            causes.append("mechanism vibration indicates stress")
            actions.append("Perform timing test and mechanism inspection")
        possible_issue = "Breaker contact heating or mechanism stress"
        reason = "The breaker is showing signs of contact degradation or mechanism abnormality."
    elif equipment_type == "Generator":
        if high_temp:
            causes.append("stator or bearing temperature is elevated")
            actions.extend([
                "Inspect bearings and rotor alignment",
                "Verify stator cooling and ventilation",
                "Check load balancing and electrical stability",
            ])
        if high_vibration:
            causes.append("rotor vibration is elevated")
            actions.append("Schedule vibration analysis")
        possible_issue = "Generator overheating or rotor imbalance"
        reason = "High vibration and temperature suggest bearing wear or rotor imbalance."
    elif equipment_type == "Motor":
        if high_temp:
            causes.append("stator temperature is elevated")
            actions.extend([
                "Inspect bearings and lubrication",
                "Check shaft alignment",
                "Verify cooling fan and ventilation",
            ])
        if high_vibration:
            causes.append("bearing vibration is abnormal")
            actions.append("Inspect winding insulation and coupling")
        if abnormal_pressure:
            actions.append("Check cooling/air pressure path")
        possible_issue = "Motor overheating or bearing wear"
        reason = "The motor is showing thermal and vibration stress consistent with bearing or alignment issues."
    elif equipment_type == "Switchgear":
        if high_temp:
            causes.append("panel hotspot temperature is rising")
            actions.extend([
                "Inspect busbar joints and panel hotspots",
                "Tighten terminations",
                "Perform thermographic inspection",
            ])
        if abnormal_pressure:
            causes.append("insulation or pressure proxy is abnormal")
            actions.append("Check insulation condition and moisture ingress")
        possible_issue = "Switchgear hotspot or insulation stress"
        reason = "The panel shows elevated thermal stress at critical connections."
    else:
        if high_temp:
            actions.append("Inspect capacitor bank cooling and thermal condition")
        if abnormal_pressure:
            actions.append("Check bank current balance and connection health")
        possible_issue = "Capacitor bank overheating or stress"
        reason = "The capacitor bank is experiencing abnormal thermal or electrical stress."

    urgency = "Low"
    inspection_window = "Next scheduled inspection"
    if risk_level == "Critical":
        urgency = "High"
        inspection_window = "Within 24 hours"
    elif risk_level == "Warning":
        urgency = "Medium"
        inspection_window = "Within 3 days"

    return {
        "equipment": equipment_name,
        "risk_level": risk_level,
        "possible_issue": possible_issue,
        "reason": reason,
        "recommended_action": list(dict.fromkeys(actions)),
        "urgency": urgency,
        "inspection_window": inspection_window,
    }


def _openai_recommendation(
    equipment_name: str,
    risk_level: str,
    temperature: float,
    vibration: float,
    pressure: float,
    health_score: float,
    failure_probability: float,
    equipment_type: Optional[str] = None,
) -> Optional[dict]:
    if not settings.openai_api_key or OpenAI is None:
        return None
    try:
        client = OpenAI(api_key=settings.openai_api_key)
        prompt = f"""You are a predictive maintenance AI assistant for electrical power equipment.

Equipment: {equipment_name}
Equipment type: {equipment_type or 'Unknown'}
Risk level: {risk_level}
Health score: {health_score}/100
Failure probability: {failure_probability}%
Temperature: {temperature}
Vibration: {vibration}
Pressure: {pressure}

Respond ONLY with valid JSON in this exact shape, no extra text:
{{
  "equipment": "string",
  "risk_level": "string",
  "possible_issue": "string",
  "reason": "string",
  "recommended_action": ["string", "string"],
  "urgency": "Low | Medium | High",
  "inspection_window": "string"
}}"""
        response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}], temperature=0.3)
        content = response.choices[0].message.content.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(content)
    except Exception:
        return None


def generate_recommendation(
    equipment_name: str,
    risk_level: str,
    temperature: float,
    vibration: float,
    pressure: float,
    health_score: float,
    failure_probability: float,
    equipment_type: Optional[str] = None,
    load: Optional[float] = None,
    rpm: Optional[float] = None,
) -> dict:
    ai_result = _openai_recommendation(
        equipment_name,
        risk_level,
        temperature,
        vibration,
        pressure,
        health_score,
        failure_probability,
        equipment_type,
    )
    if ai_result:
        return ai_result
    return _rule_based_recommendation(
        equipment_name,
        risk_level,
        temperature,
        vibration,
        pressure,
        equipment_type=equipment_type,
        health_score=health_score,
        failure_probability=failure_probability,
    )
