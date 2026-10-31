"""Core data models for Open AI Governance Feed."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


ALLOWED_RISK_RATINGS = {"unknown", "low", "medium", "high"}


@dataclass
class GovernanceRecord:
    """A single AI service observation used for governance purposes."""

    tool_name: str
    domain: str
    category: str
    sources: list[str] = field(default_factory=list)
    risk_rating: str = "unknown"
    last_seen: date | None = None
    notes: str = ""
