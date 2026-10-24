from models import Intake
from parser import parse_text
from rules import analyze, bleeding_score


def test_missing_counts_are_not_zero():
    d = Intake(cycle_length_days=45, notes="heavy bleeding")
    assert bleeding_score(d) is None
    assert analyze(d).bleeding_score is None


def test_cycle_and_qualitative_symptoms():
    text = "Main concern: Multiple concerns\nDescription: My periods are very heavy and painful, and my cycle is 45 days long.\nDuration: More than 3 months\nCycle pattern: Changes month to month\nPain: Very painful"
    parsed = parse_text(text)
    assert parsed["ok"] is True
    d = Intake(**parsed["intake"])
    result = analyze(d)
    assert d.cycle_length_days == 45
    assert result.bleeding_score is None
    assert any("45 days" in f.text for f in result.findings)
    assert any("heavy menstrual bleeding" in f.text for f in result.findings)
    assert any("very painful" in f.text.lower() for f in result.findings)


def test_hourly_pad_flag():
    parsed = parse_text("I am soaking through a pad every hour and feel faint")
    assert len(parsed["red_flags"]) >= 2
    result = analyze(Intake(**parsed["intake"]))
    assert result.red_flag is True
    assert "urgent" in result.safety_guidance.lower()


def test_complete_counts_calculate_score():
    d = Intake(pads_light=2, pads_moderate=6, pads_heavy=4, clots_small=0, clots_large=2, flooding=2)
    assert bleeding_score(d) == 2 + 5*6 + 20*4 + 0 + 5*2 + 5*2


def test_exact_user_example_preserves_heavy_and_painful_symptoms():
    text = "My periods are very heavy and painful, and my cycle is 45 days long."
    parsed = parse_text(text)
    d = Intake(**parsed["intake"])
    result = analyze(d)
    assert d.cycle_length_days == 45
    assert d.pain_score is None
    assert result.bleeding_score is None
    assert any("heavy menstrual bleeding" in f.text for f in result.findings)
    assert any("very painful" in f.text.lower() for f in result.findings)
