"""
Core data models for PhysiCards.
"""

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Deck:
    id: str
    name: str
    description: str
    icon: str = "atom"
    color: str = "#3b82f6"
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Card:
    id: str
    deck_id: str
    title: str
    front: str
    back: str
    hint: str = ""
    formula_breakdown: str = ""  # Variable & Unit explanations (Markdown / LaTeX)
    physical_meaning: str = ""  # Physical background & interpretation
    validity_domain: str = ""  # Limits & assumptions (e.g. non-relativistic, ideal gas)
    tags: list[str] = field(default_factory=list)
    difficulty: int = 3  # 1 (Leicht) to 5 (Sehr anspruchsvoll)
    has_cloze: bool = False  # Contains {{c1::...}} cloze deletions
    created_at: str = field(default_factory=now_iso)
    updated_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ReviewState:
    card_id: str
    repetitions: int = 0
    interval_days: float = 0.0
    ease_factor: float = 2.5
    next_due: str = field(default_factory=now_iso)
    last_reviewed: str | None = None
    total_reviews: int = 0
    lapses: int = 0
    last_quality: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class StudyLog:
    id: int | None
    card_id: str
    deck_id: str
    quality: int
    interval_days: float
    ease_factor: float
    response_time_ms: int = 0
    timestamp: str = field(default_factory=now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
