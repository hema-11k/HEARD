
import os

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from models import Intake, Result
from rules import analyze
from parser import parse_text


app = FastAPI(title="Heard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:3000,http://localhost:5000,http://127.0.0.1:5000"
    ).split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)


class ParseIn(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)


class AssessResponse(BaseModel):
    parsed_intake: Intake
    analysis: Result


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/parse")
def parse(body: ParseIn):
    return parse_text(body.text)


@app.post("/analyze", response_model=Result)
def analyze_intake(intake: Intake):
    return analyze(intake)


@app.post("/assess", response_model=AssessResponse)
def assess(body: ParseIn):
    parsed = parse_text(body.text)

    if not parsed.get("ok") or not parsed.get("intake"):
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Could not read this intake. Please add a little more detail and try again.",
                "reason": parsed.get("reason", "Parsing unsuccessful."),
                "red_flags": parsed.get("red_flags", []),
            },
        )

    intake = Intake(**parsed["intake"])
    result = analyze(intake)

    return AssessResponse(
        parsed_intake=intake,
        analysis=result,
    )


DEMO = Intake(
    cycle_length_days=45,
    period_duration_days=9,
    cycle_day_today=10,
    planned_test="FSH / LH / Estradiol",
    pads_light=2,
    pads_moderate=6,
    pads_heavy=4,
    clots_small=0,
    clots_large=2,
    flooding=2,
    pain_score=7,
    pain_location="Pelvic",
    pain_timing="During period",
    fatigue=True,
    notes="Periods very heavy and painful for 2 years.",
)


@app.get("/demo", response_model=Result)
def demo():
    return analyze(DEMO)
