from pydantic import BaseModel


class MissionTelemetry(BaseModel):
    altitude_m: float
    velocity_mps: float
    battery_pct: float
    wind_kph: float
    target_distance_m: float
    destination: str


class MissionOutcome(BaseModel):
    success: bool
    battery_pct: float
    risk_index: float
    route_efficiency: float
