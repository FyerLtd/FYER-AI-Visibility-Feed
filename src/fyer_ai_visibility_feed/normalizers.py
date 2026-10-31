"""Normalization helpers for FYER AI Visibility Feed."""

from __future__ import annotations


def normalize_domain(domain: str) -> str:
    """Return a conservative canonical representation of a hostname."""

    normalized = domain.strip().lower()

    # A trailing dot represents the DNS root and is not useful
    # in the governance feed's canonical hostname representation.
    normalized = normalized.rstrip(".")

    # Treat the conventional www hostname as the same web service
    # hostname for catalogue purposes.
    if normalized.startswith("www."):
        normalized = normalized[4:]

    return normalized
