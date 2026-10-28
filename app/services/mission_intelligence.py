from dataclasses import dataclass, field
from typing import List


@dataclass
class RouteDecision:
    route: str
    confidence: float
    mode: str
    actions: List[str] = field(default_factory=list)
    wake_window: str = "05:30 - 06:10"


class MissionIntelligence:
    def __init__(self) -> None:
        self.mission_history: List[dict] = []

    def _assess_weather(self, weather: str) -> float:
        risk_map = {
            "clear": 0.10,
            "light_cloud": 0.15,
            "windy": 0.28,
            "rain": 0.40,
            "storm": 0.72,
        }
        return risk_map.get(weather.lower(), 0.20)

    def plan_mission(
        self,
        location: str,
        user_home: str,
        tea_order: str,
        weather: str,
        time_of_day: str,
        risk_threshold: float,
    ) -> RouteDecision:
        environmental_risk = self._assess_weather(weather)
        risk_margin = max(0.0, environmental_risk - risk_threshold)

        if risk_margin > 0.18:
            route = f"safe-corridor->{location}"
            mode = "conservative"
            actions = [
                "increase altitude buffer",
                "delay descent near restaurant",
                "verify landing zone with vision",
                "return with caution if risk spikes",
            ]
            confidence = 0.78
        else:
            route = f"direct-route->{location}"
            mode = "adaptive"
            actions = [
                "navigate to pickup point",
                "scan restaurant zone",
                "confirm tea order and payload",
                "return to home with wake-window synchronization",
            ]
            confidence = 0.88

        decision = RouteDecision(
            route=route,
            confidence=confidence,
            mode=mode,
            actions=actions,
            wake_window=f"{time_of_day} - {self._wake_window(time_of_day)}",
        )
        self.mission_history.append(
            {
                "location": location,
                "weather": weather,
                "route": route,
                "confidence": confidence,
                "tea_order": tea_order,
                "home": user_home,
            }
        )
        return decision

    def _wake_window(self, time_of_day: str) -> str:
        try:
            hour = int(time_of_day.split(":")[0])
            updated = hour + 1
            return f"{updated:02d}:10"
        except ValueError:
            return "06:10"

    def summary(self) -> dict:
        if not self.mission_history:
            return {"missions": 0, "status": "waiting_for_first_plan"}
        latest = self.mission_history[-1]
        return {
            "missions": len(self.mission_history),
            "status": "operational",
            "latest_route": latest["route"],
            "latest_weather": latest["weather"],
            "latest_confidence": round(latest["confidence"], 2),
        }

    def evaluate_outcome(self, outcome: dict) -> float:
        success = outcome.get("success", False)
        battery_penalty = 0.05 * max(0, 50 - float(outcome.get("battery_pct", 50))) / 50
        risk_penalty = 0.08 * float(outcome.get("risk_index", 0.0))
        if success:
            return 1.0 - battery_penalty - risk_penalty
        return -1.0 + battery_penalty + risk_penalty
