from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


class Intake(BaseModel):
    cycle_length_days: Optional[int] = Field(None, ge=1, le=120)
    period_duration_days: Optional[int] = Field(None, ge=1, le=60)
    cycle_day_today: Optional[int] = Field(None, ge=1, le=120)
    planned_test: Optional[str] = None
    last_period_start: Optional[date] = None  # YYYY-MM-DD, powers the test-timing planner

    pads_light: Optional[int] = Field(None, ge=0, le=100)
    pads_moderate: Optional[int] = Field(None, ge=0, le=100)
    pads_heavy: Optional[int] = Field(None, ge=0, le=100)
    clots_small: Optional[int] = Field(None, ge=0, le=100)
    clots_large: Optional[int] = Field(None, ge=0, le=100)
    flooding: Optional[int] = Field(None, ge=0, le=100)

    # None means the user did not provide a numeric pain score.
    pain_score: Optional[int] = Field(None, ge=0, le=10)
    pain_location: str = ""
    pain_timing: str = ""
    fatigue: bool = False
    red_flags: list[str] = Field(default_factory=list)
    notes: str = Field("", max_length=2000)


class Finding(BaseModel):
    text: str
    source: str


class TimingCheck(BaseModel):
    test: str
    ok: bool
    note: str
    source: str
    window_start: Optional[date] = None
    window_end: Optional[date] = None
    window_text: str = ""


class Result(BaseModel):
    red_flag: bool
    red_flags: list[str]
    safety_guidance: str
    bleeding_score: Optional[int]
    findings: list[Finding]
    timing: Optional[TimingCheck]
    questions_for_doctor: list[str]
    advocacy_line: str
    disclaimer: str