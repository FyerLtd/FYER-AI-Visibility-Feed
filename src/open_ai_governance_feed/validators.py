"""Validation rules for governance records."""

from __future__ import annotations

import re
from urllib.parse import urlparse

from .models import ALLOWED_RISK_RATINGS, GovernanceRecord


DOMAIN_PATTERN = re.compile(
    r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+"
    r"[a-zA-Z]{2,63}$"
)


def validate_record(record: GovernanceRecord) -> list[str]:
    """Return validation errors for a governance record."""

    errors: list[str] = []

    if not record.tool_name.strip():
        errors.append("tool_name is required")

    domain = record.domain.strip().lower()

    if not domain:
        errors.append("domain is required")
    elif not DOMAIN_PATTERN.fullmatch(domain):
        errors.append("domain must be a valid hostname")

    if not record.category.strip():
        errors.append("category is required")

    if not record.sources:
        errors.append("at least one source is required")
    else:
        for source in record.sources:
            parsed = urlparse(source)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                errors.append("sources must contain valid HTTP or HTTPS URLs")
                break

    if record.risk_rating not in ALLOWED_RISK_RATINGS:
        errors.append(
            "risk_rating must be one of: unknown, low, medium, high"
        )

    return errors
