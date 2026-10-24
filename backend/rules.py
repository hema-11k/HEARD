import re
from models import Intake, Finding, Result
from timing import check_timing

DISCLAIMER = (
    "HEARD does not diagnose or replace a clinician. It organizes the information you shared "
    "to help you discuss symptoms with a qualified healthcare professional."
)


def bleeding_score(d: Intake):
    """Return None unless every required count was actually provided."""
    values = [d.pads_light, d.pads_moderate, d.pads_heavy, d.clots_small, d.clots_large, d.flooding]
    if any(value is None for value in values):
        return None
    return d.pads_light + 5*d.pads_moderate + 20*d.pads_heavy + d.clots_small + 5*d.clots_large + 5*d.flooding


def analyze(d: Intake) -> Result:
    findings, questions = [], []
    score = bleeding_score(d)
    counts_complete = score is not None
    iron_risk = False
    cycle_length = d.cycle_length_days
    notes = d.notes.lower()

    if cycle_length is not None and (cycle_length < 21 or cycle_length > 35):
        findings.append(Finding(text=f"Cycle length {cycle_length} days is outside the typical 21–35 day range.", source="General adult menstrual-cycle guidance; discuss individual context with a clinician."))
        questions.append(f"My cycles are {cycle_length} days. What could explain this pattern?")

    if d.period_duration_days is not None and d.period_duration_days > 7:
        findings.append(Finding(text=f"Periods lasting {d.period_duration_days} days may be prolonged.", source="General menstrual-health guidance; not a diagnosis."))
        iron_risk = True

    # Preserve qualitative symptom reports without pretending they are numeric scores.
    heavy_reported = bool(re.search(r"\bheavy bleeding\b|\bvery heavy\b|\bperiods? (?:are|is) heavy\b|\bheavy (?:periods?|flow)\b", notes))
    painful_reported = bool(re.search(r"\bvery painful\b|\bsevere pain\b|\bperiods? (?:are|is) painful\b|\bperiods?\b.{0,60}\bpainful\b|\bextremely painful\b|\bsevere cramps?\b", notes))

    if heavy_reported:
        findings.append(Finding(text="You reported heavy menstrual bleeding. The pad/clot counts needed for a numeric screening estimate were not all provided, so no bleeding score is calculated.", source="User-reported symptom; a clinician can assess severity and possible causes."))
        questions.append("Could we assess the amount of bleeding and whether a blood count or iron testing is appropriate?")
        iron_risk = True

    if counts_complete and score > 100:
        findings.append(Finding(text=f"Calculated bleeding screening score: {score}. This may warrant discussion of heavy bleeding.", source="Screening estimate only; not a diagnosis."))
        questions.append("Could we discuss this bleeding estimate and possible causes?")
        iron_risk = True
    elif counts_complete:
        findings.append(Finding(text=f"Calculated bleeding screening score: {score} based on the counts entered.", source="Screening estimate only; it cannot rule out a health problem."))

    if d.pain_score is not None and (d.pain_score >= 7 or (d.pain_score >= 4 and d.pain_timing)):
        location = f" ({d.pain_location.lower()})" if d.pain_location else ""
        timing = f", {d.pain_timing.lower()}" if d.pain_timing else ""
        findings.append(Finding(text=f"Pain reported as {d.pain_score}/10{location}{timing}.", source="Significant or recurring pain may warrant clinical evaluation."))
        questions.append("What could be causing this pain, and what should we do next?")
    elif painful_reported:
        findings.append(Finding(text="You described your periods as very painful. A numeric pain score was not provided, so none has been assumed.", source="User-reported symptom; significant or recurring pain may warrant clinical evaluation."))
        questions.append("What could be causing this pain, and what options are appropriate for me?")

    if d.fatigue and iron_risk:
        findings.append(Finding(text="Fatigue together with reported heavy or prolonged bleeding may warrant assessment for iron deficiency.", source="Possible risk only; testing and clinical interpretation are needed."))
        questions.append("Would checking haemoglobin and ferritin be appropriate?")

    if d.red_flags:
        findings.append(Finding(text="A potential warning symptom was reported: " + ", ".join(d.red_flags) + ".", source="Based on the symptom description; this is not a diagnosis."))

    questions.extend(["What would make you consider further testing?", "Can you note in my file that I raised this today?"])
    if d.red_flags:
        safety = "A warning symptom was detected. Seek urgent medical assessment now, especially if bleeding is soaking a pad each hour, you faint or feel severely dizzy, have sudden severe pain, or pregnancy is possible with pain/bleeding. Contact local emergency services if symptoms are severe."
    else:
        safety = "No specific urgent warning pattern was detected in the text provided. This does not rule out a problem. Seek urgent care if you develop very heavy bleeding (such as soaking a pad each hour), fainting/severe dizziness, sudden severe pain, or pain/bleeding when pregnancy is possible."

    return Result(
        red_flag=bool(d.red_flags), red_flags=d.red_flags, safety_guidance=safety,
        bleeding_score=score, findings=findings,
        timing=check_timing(d.planned_test, d.cycle_day_today, cycle_length),
        questions_for_doctor=questions,
        advocacy_line="I understand symptoms can be common, but they are affecting my life. What is the next step if this continues?",
        disclaimer=DISCLAIMER,
    )
