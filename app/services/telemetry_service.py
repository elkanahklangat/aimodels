from typing import Any, Dict


class TelemetryService:
    def summarize(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "altitude_m": float(payload.get("altitude_m", 0.0)),
            "velocity_mps": float(payload.get("velocity_mps", 0.0)),
            "battery_pct": float(payload.get("battery_pct", 100.0)),
            "wind_kph": float(payload.get("wind_kph", 0.0)),
            "target_distance_m": float(payload.get("target_distance_m", 0.0)),
            "status": payload.get("status", "in_flight"),
            "destination": payload.get("destination", "unknown"),
        }
