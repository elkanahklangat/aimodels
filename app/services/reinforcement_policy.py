from typing import Dict, Any


class ReinforcementPolicy:
    def __init__(self) -> None:
        self.policy = {
            "reward": 0.0,
            "risk_bias": 0.0,
            "confidence_bias": 0.0,
            "mission_count": 0,
        }

    def evaluate_telemetry(self, telemetry: Dict[str, Any]) -> Dict[str, Any]:
        risk_score = 0.0
        if telemetry.get("wind_kph", 0) > 15:
            risk_score += 0.25
        if telemetry.get("battery_pct", 100) < 30:
            risk_score += 0.25
        if telemetry.get("target_distance_m", 0) > 1000:
            risk_score += 0.15

        confidence = max(0.0, 1.0 - risk_score)
        return {
            "risk_score": round(risk_score, 3),
            "confidence": round(confidence, 3),
            "action": "safe-corridor" if risk_score > 0.35 else "adaptive-route",
        }

    def update_from_outcome(self, outcome: Dict[str, Any]) -> float:
        result = float(outcome.get("reward", 0.0))
        self.policy["reward"] = (self.policy["reward"] * self.policy["mission_count"] + result) / max(1, self.policy["mission_count"] + 1)
        self.policy["mission_count"] += 1
        self.policy["risk_bias"] = min(1.0, max(0.0, self.policy["risk_bias"] + result * 0.05))
        self.policy["confidence_bias"] = min(1.0, max(0.0, self.policy["confidence_bias"] + (0.5 if result > 0 else -0.1)))
        return round(self.policy["reward"], 3)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "reward": round(self.policy["reward"], 3),
            "risk_bias": round(self.policy["risk_bias"], 3),
            "confidence_bias": round(self.policy["confidence_bias"], 3),
            "mission_count": self.policy["mission_count"],
        }
