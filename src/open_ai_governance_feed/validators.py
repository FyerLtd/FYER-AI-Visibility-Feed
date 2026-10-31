"""Validation rules for governance records and source policies."""

from __future__ import annotations

import re
from urllib.parse import urlparse

from .models import (
    ALLOWED_COLLECTION_METHODS,
    ALLOWED_COLLECTION_STATUSES,
    ALLOWED_RISK_RATINGS,
    GovernanceRecord,
    SourcePolicy,
)


DOMAIN_PATTERN = re.compile(
    r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+"
    r"[a-zA-Z]{2,63}$"
)


def _is_http_url(value: str) -> bool:
    """Return whether a value is an HTTP or HTTPS URL."""

    parsed = urlparse(value)

    return (
        parsed.scheme in {"http", "https"}
        and bool(parsed.netloc)
    )


def validate_evidence(record: GovernanceRecord) -> list[str]:
    """Return validation errors for structured source evidence."""

    errors: list[str] = []

    for evidence in record.evidence:
        if not evidence.source_name.strip():
            errors.append("evidence source_name is required")

        if not _is_http_url(evidence.source_url):
            errors.append(
                "evidence source_url must be a valid HTTP or HTTPS URL"
            )

    return errors


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
            if not _is_http_url(source):
                errors.append(
                    "sources must contain valid HTTP or HTTPS URLs"
                )
                break

    if record.risk_rating not in ALLOWED_RISK_RATINGS:
        errors.append(
            "risk_rating must be one of: unknown, low, medium, high"
        )

    errors.extend(validate_evidence(record))

    return errors

def validate_source_policy(
    policy: SourcePolicy,
) -> list[str]:
    """Return validation errors for a source policy."""

    errors: list[str] = []

    if not policy.name.strip():
        errors.append("source name is required")

    if not _is_http_url(policy.homepage_url):
        errors.append(
            "homepage_url must be a valid HTTP or HTTPS URL"
        )

    if policy.collection_status not in ALLOWED_COLLECTION_STATUSES:
        errors.append(
            "collection_status must be one of: "
            "pending-review, approved, prohibited"
        )

    if policy.collection_method not in ALLOWED_COLLECTION_METHODS:
        errors.append(
            "collection_method must be one of: "
            "manual, api, html, feed"
        )

    if policy.terms_url is not None:
        if not _is_http_url(policy.terms_url):
            errors.append(
                "terms_url must be a valid HTTP or HTTPS URL"
            )

    if policy.robots_url is not None:
        if not _is_http_url(policy.robots_url):
            errors.append(
                "robots_url must be a valid HTTP or HTTPS URL"
            )

    if policy.collection_status == "approved":
        if policy.reviewed_at is None:
            errors.append(
                "approved sources require reviewed_at"
            )

        if not policy.reviewer:
            errors.append(
                "approved sources require reviewer"
            )
        elif not policy.reviewer.strip():
            errors.append(
                "approved sources require reviewer"
            )

if not policy.permitted_metadata:
    errors.append(
        "approved sources require permitted_metadata"
    )

        automated_methods = {
            "api",
            "html",
            "feed",
        }

        if policy.collection_method in automated_methods:
            if policy.terms_url is None:
                errors.append(
                    "approved automated sources require terms_url"
                )

        if policy.collection_method == "html":
            if policy.robots_url is None:
                errors.append(
                    "approved HTML sources require robots_url"
                )

    return errors

def source_is_collection_eligible(
    policy: SourcePolicy,
) -> bool:
    """Return whether a source is eligible for collection."""

    if policy.collection_status != "approved":
        return False

    return validate_source_policy(policy) == []
