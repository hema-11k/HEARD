from datetime import date, timedelta
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


def _window(test, lps, cycle_length):
    """Best window (start, end) in the cycle that began on lps. Cycle day N = lps + (N-1)."""
    if test == "FSH / LH / Estradiol":
        return lps + timedelta(days=1), lps + timedelta(days=4)  # cycle days 2-5
    if test == "Progesterone":
        if cycle_length is None or not 21 <= cycle_length <= 35:
            return None  # unreliable for irregular cycles
        t = cycle_length - 7
        return lps + timedelta(days=t - 2), lps + timedelta(days=t)  # days t-1 .. t+1
    return None  # TSH, prolactin, ferritin/CBC: no fixed day


def plan_window(test, lps, cycle_length, today=None):
    """Next usable window on or after today; rolls into the next cycle if this one has passed."""
    today = today or date.today()
    w = _window(test, lps, cycle_length)
    if not w:
        return None
    start, end = w
    n = 0
    while end < today and cycle_length and n < 12:
        start, end, n = start + timedelta(days=cycle_length), end + timedelta(days=cycle_length), n + 1
    return None if end < today else (start, end)


def check_timing(
    test: Optional[str],
    day: Optional[int],
    cycle_len: Optional[int],
    last_period_start: Optional[date] = None,
    today: Optional[date] = None,
) -> Optional[TimingCheck]:

    if not test or test not in TESTS:
        return None
    today = today or date.today()
    if not day and last_period_start:
        day = (today - last_period_start).days + 1
    if not day or day < 1 or day > 120:
        return None

    timing_function, source = TESTS[test]
    ok, note = timing_function(day, cycle_len)

    start = end = None
    text = "Any cycle day" if test in ("TSH", "Prolactin", "Ferritin / CBC") else ""
    if last_period_start:
        w = plan_window(test, last_period_start, cycle_len, today)
        if w:
            start, end = w
            text = f"Book between {start.day} {start:%b} and {end.day} {end:%b}"

    return TimingCheck(test=test, ok=ok, note=note, source=source,
                       window_start=start, window_end=end, window_text=text)