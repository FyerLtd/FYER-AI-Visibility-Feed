"""Core data models for Open AI Governance Feed."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime


ALLOWED_RISK_RATINGS = {"unknown", "low", "medium", "high"}

ALLOWED_COLLECTION_STATUSES = {
    "pending-review",
    "approved",
    "prohibited",
}

ALLOWED_COLLECTION_METHODS = {
    "manual",
    "api",
    "html",
    "feed",
}


@dataclass(frozen=True)
class SourceEvidence:
    """Provenance for a single public-source observation."""

    source_name: str
    source_url: str
    observed_at: datetime


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
    evidence: list[SourceEvidence] = field(default_factory=list)


@dataclass(frozen=True)
class RecordConflict:
    """A disagreement between observations for one canonical domain."""

    domain: str
    field_name: str
    observed_values: tuple[str, ...]
    sources: tuple[str, ...]


@dataclass
class SourcePolicy:
    """Governance policy for a potential public metadata source."""

    name: str
    homepage_url: str
    collection_status: str = "pending-review"
    collection_method: str = "manual"
    terms_url: str | None = None
    robots_url: str | None = None
    permitted_metadata: list[str] = field(default_factory=list)
    reviewed_at: date | None = None
    reviewer: str | None = None
    notes: str = ""
