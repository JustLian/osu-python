import typing as t


def calculate_ar(ar: float) -> t.Tuple[int, int]:
    """Calculates preempt and fade_in time from AR"""
    if ar < 5:
        return (1200 + 600 * (5 - ar) / 5, 800 + 400 * (5 - ar) / 5)

    if ar == 5:
        return (1200, 800)

    if ar > 5:
        return (1200 - 750 * (ar - 5) / 5, 800 - 500 * (ar - 5) / 5)
