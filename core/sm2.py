"""
SuperMemo SM-2 Spaced Repetition Algorithm implementation for PhysiCards.
Calculates next review intervals, ease factor adjustments, and provides
interval preview estimates for the UI.
"""

from datetime import datetime, timedelta, timezone

from core.models import ReviewState

MIN_EASE_FACTOR = 1.3
DEFAULT_EASE_FACTOR = 2.5


def calculate_sm2(state: ReviewState, rating: int) -> tuple[ReviewState, float]:
    """
    Update review state according to SM-2 algorithm.
    Rating scale (1-4 from UI):
      1: Nochmal (Lapse, failed recall)
      2: Schwer (Hard, remembered with difficulty)
      3: Gut (Good, correct recall with reasonable effort)
      4: Einfach (Easy, instantaneous perfect recall)

    Returns:
      (updated_state, interval_days)
    """
    # Map 1-4 UI rating to standard SM-2 0-5 scale:
    # 1 -> 1 (Incorrect, failed)
    # 2 -> 3 (Correct, serious difficulty)
    # 3 -> 4 (Correct after hesitation)
    # 4 -> 5 (Perfect recall)
    q_map = {1: 1, 2: 3, 3: 4, 4: 5}
    q = q_map.get(rating, 4)

    now = datetime.now(timezone.utc)
    new_state = ReviewState(
        card_id=state.card_id,
        repetitions=state.repetitions,
        interval_days=state.interval_days,
        ease_factor=state.ease_factor,
        next_due=state.next_due,
        last_reviewed=now.isoformat(),
        total_reviews=state.total_reviews + 1,
        lapses=state.lapses,
        last_quality=rating,
    )

    # Ease factor update formula:
    # EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
    ef_change = 0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)
    new_ef = max(MIN_EASE_FACTOR, round(state.ease_factor + ef_change, 3))
    new_state.ease_factor = new_ef

    if rating == 1:
        # Failed recall / lapse
        new_state.repetitions = 0
        new_state.lapses += 1
        # Due again in 10 minutes (0.007 days) or same session
        interval_days = 0.007
        next_due_dt = now + timedelta(minutes=10)
    else:
        # Successful recall
        if state.repetitions == 0:
            if rating == 2 or rating == 3:
                interval_days = 1.0
            else:  # rating == 4 (Easy)
                interval_days = 3.0
            new_state.repetitions = 1
        elif state.repetitions == 1:
            if rating == 2:
                interval_days = 2.0
            elif rating == 3:
                interval_days = 6.0
            else:  # rating == 4 (Easy)
                interval_days = 8.0
            new_state.repetitions = 2
        else:
            # rep >= 2
            prev_interval = max(1.0, state.interval_days)
            if rating == 2:
                # Hard: smaller growth
                interval_days = round(prev_interval * 1.2, 1)
            elif rating == 3:
                # Good: standard EF multiplier
                interval_days = round(prev_interval * new_ef, 1)
            else:
                # Easy: EF multiplier with extra bonus
                interval_days = round(prev_interval * new_ef * 1.3, 1)
            new_state.repetitions = state.repetitions + 1

        next_due_dt = now + timedelta(days=interval_days)

    new_state.interval_days = interval_days
    new_state.next_due = next_due_dt.isoformat()

    return new_state, interval_days


def format_interval(days: float) -> str:
    """Format an interval in days into a user-friendly German string."""
    if days < 0.02:
        return "< 10 Min"
    elif days < 1.0:
        hours = max(1, int(days * 24))
        return f"{hours} Std"
    elif days < 30.0:
        d = int(round(days))
        return f"{d} Tag" if d == 1 else f"{d} Tage"
    elif days < 365.0:
        months = int(round(days / 30.0))
        return f"{months} Mon"
    else:
        years = round(days / 365.0, 1)
        return f"{years} Jahre"


def predict_intervals(state: ReviewState) -> dict[int, str]:
    """
    Returns a dictionary of preview labels for ratings 1-4.
    e.g. {1: '< 10 Min', 2: '2 Tage', 3: '5 Tage', 4: '10 Tage'}
    """
    previews = {}
    for r in [1, 2, 3, 4]:
        _, days = calculate_sm2(state, r)
        previews[r] = format_interval(days)
    return previews
