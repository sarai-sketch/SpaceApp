from pydantic import BaseModel, Field
from typing import Literal

class Scenario(BaseModel):
    rain_change_pct: float = Field(40, ge=-100, le=500)
    temp_delta_c: float = Field(-8, ge=-30, le=30)
    duration_days: int = Field(3, ge=1, le=90)
    baseline_rain_mm_day: float = Field(5, ge=0, le=500)
    baseline_temp_c: float = Field(12, ge=-40, le=60)
    eto_mm_day: float = Field(2, ge=0, le=20)
    soil_moisture: float = Field(.24, ge=0, le=.8)
    field_capacity: float = Field(.30, ge=.01, le=.8)
    wilting_point: float = Field(.15, ge=0, le=.7)
    root_depth_m: float = Field(.5, gt=0, le=4)
    kc: float = Field(.8, ge=0, le=2)
    p_fraction: float = Field(.5, ge=.05, le=.95)
    runoff_fraction: float = Field(.10, ge=0, le=1)
    irrigation_mm_day: float = Field(0, ge=0, le=100)
    crop_stage: Literal['emergencia','vegetativo','floracion','llenado'] = 'vegetativo'

class SensorReading(BaseModel):
    device_id: str
    temperature_c: float
    moisture_pct: float = Field(ge=0, le=100)
    ec_ms_cm: float | None = None
    timestamp: str | None = None

class ChatInput(BaseModel):
    question: str
    scenario: Scenario | None = None
