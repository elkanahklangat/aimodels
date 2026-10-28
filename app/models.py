from pydantic import BaseModel


class MissionTelemetry(BaseModel):
    altitude_m: float
    velocity_mps: float
    battery_pct: float
    wind_kph: float
    target_distance_m: float
    destination: str
