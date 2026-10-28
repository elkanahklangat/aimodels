from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.services.mission_intelligence import MissionIntelligence

app = FastAPI(
    title="Aero-Delivery Intelligence API",
    version="0.1.0",
    description="Mission-aware intelligence for autonomous aerial tea delivery and adaptive flight behavior.",
)

intelligence = MissionIntelligence()


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
        ],
    }
