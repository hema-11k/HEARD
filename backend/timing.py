
from typing import Optional
from models import TimingCheck


ANYDAY = "No fixed menstrual cycle day is generally required."


def baseline(day, cycle_length):
    if 2 <= day <= 5:
        return True, (
            f"Cycle day {day} falls within the commonly used "
            "baseline window (days 2-5). Confirm with your clinician."
        )

    return False, (
        f"Cycle day {day} is outside the commonly used baseline "
        "window. Ask your clinician whether different timing is needed."
    )


def progesterone(day, cycle_length):
    if cycle_length is None or not 21 <= cycle_length <= 35:
        return False, (
            "A fixed cycle-day estimate may be unreliable. "
            "Ask your clinician how to time this test based on ovulation."
        )

    target = cycle_length - 7

    if abs(day - target) <= 1:
        return True, (
            f"Cycle day {day} is near the estimated mid-luteal "
            f"window (around day {target}). Confirm the timing with your clinician."
        )

    return False, (
        f"For a {cycle_length}-day cycle, day {target} is an estimate "
        "for the mid-luteal window. Actual timing depends on ovulation."
    )


TESTS = {
    "FSH / LH / Estradiol": (
        baseline,
        "Baseline timing varies by clinical purpose; confirm with clinician."
    ),
    "Progesterone": (
        progesterone,
        "Timing depends on ovulation and the expected next period."
    ),
    "TSH": (
        lambda day, length: (True, ANYDAY),
        "No fixed menstrual cycle day is generally required."
    ),
    "Prolactin": (
        lambda day, length: (
            True,
            ANYDAY + " Follow laboratory instructions about collection time and preparation."
        ),
        "Follow laboratory and clinician instructions."
    ),
    "Ferritin / CBC": (
        lambda day, length: (True, ANYDAY),
        "Follow laboratory instructions."
    ),
}


def check_timing(
    test: Optional[str],
    day: Optional[int],
    cycle_len: Optional[int]
) -> Optional[TimingCheck]:

    if not test or not day or test not in TESTS:
        return None

    if day < 1 or day > 120:
        return None

    timing_function, source = TESTS[test]
    ok, note = timing_function(day, cycle_len)

    return TimingCheck(
        test=test,
        ok=ok,
        note=note,
        source=source
    )
