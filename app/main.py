from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.services.mission_intelligence import MissionIntelligence
from app.services.reinforcement_policy import ReinforcementPolicy
from app.services.telemetry_service import TelemetryService

app = FastAPI(
    title="Aero-Delivery Intelligence API",
    version="0.1.0",
    description="Mission-aware intelligence for autonomous aerial tea delivery and adaptive flight behavior.",
)

intelligence = MissionIntelligence()
policy = ReinforcementPolicy()
telemetry_service = TelemetryService()


class MissionRequest(BaseModel):
    location: str = Field(..., description="Pickup destination or restaurant")
    user_home: str = Field(..., description="Home or final drop-off location")
    tea_order: str = Field(..., description="Tea selection or desired drink")
    weather: str = Field(..., description="Current environmental state")
    time_of_day: str = Field(default="05:30", description="Planned mission time")
    risk_threshold: float = Field(default=0.22, ge=0.0, le=1.0)


class MissionResponse(BaseModel):
    route: str
    confidence: float
    mode: str
    actions: list[str]
    wake_window: str


class TelemetryEvent(BaseModel):
    altitude_m: float
    velocity_mps: float
    battery_pct: float
    wind_kph: float
    target_distance_m: float
    destination: str
    status: str = "in_flight"


@app.get("/health")
async def health() -> dict:
    return {
        "status": "ok",
        "service": "aero-delivery-intelligence",
        "mode": "adaptive",
    }


@app.post("/mission/planning", response_model=MissionResponse)
async def plan_mission(request: MissionRequest) -> MissionResponse:
    return intelligence.plan_mission(
        location=request.location,
        user_home=request.user_home,
        tea_order=request.tea_order,
        weather=request.weather,
        time_of_day=request.time_of_day,
        risk_threshold=request.risk_threshold,
    )


@app.get("/mission/summary")
async def mission_summary() -> dict:
    return intelligence.summary()


@app.post("/telemetry/ingest")
async def ingest_telemetry(event: TelemetryEvent) -> dict:
    metrics = telemetry_service.summarize(event.model_dump())
    return {
        "status": "accepted",
        "metrics": metrics,
        "learning_signal": policy.evaluate_telemetry(metrics),
    }


@app.post("/learning/reward")
async def learning_reward(payload: dict) -> dict:
    reward = policy.update_from_outcome(payload)
    return {
        "status": "updated",
        "reward": reward,
        "policy_snapshot": policy.snapshot(),
    }


@app.get("/learning/policy")
async def policy_state() -> dict:
    return policy.snapshot()


@app.get("/")
async def root() -> dict:
    return {
        "project": "Aero-Delivery Intelligence",
        "status": "ready",
        "linked_repo": "Pyv",
        "capabilities": [
            "route planning",
            "risk-aware mission logic",
            "vision-driven perception",
            "adaptive behavior",
            "telemetry learning",
            "policy optimization",
        ],
    }
