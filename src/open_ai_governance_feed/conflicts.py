"""Conflict detection for governance observations."""

from __future__ import annotations

from collections import defaultdict

from .models import GovernanceRecord, RecordConflict
from .normalizers import normalize_domain


CONFLICT_FIELDS = (
    "tool_name",
    "category",
    "risk_rating",
)


def detect_conflicts(
    records: list[GovernanceRecord],
) -> list[RecordConflict]:
    """Return disagreements between records sharing a canonical domain.

    Conflict detection reports differences without deciding which
    observation is correct.
    """

    grouped_records: dict[str, list[GovernanceRecord]] = defaultdict(list)

    for record in records:
        canonical_domain = normalize_domain(record.domain)
        grouped_records[canonical_domain].append(record)

    conflicts: list[RecordConflict] = []

    for canonical_domain, domain_records in grouped_records.items():
        if len(domain_records) < 2:
            continue

        all_sources = tuple(
            dict.fromkeys(
                source
                for record in domain_records
                for source in record.sources
            )
        )

        for field_name in CONFLICT_FIELDS:
            observed_values = tuple(
                dict.fromkeys(
                    str(getattr(record, field_name)).strip()
                    for record in domain_records
                )
            )

            if len(observed_values) > 1:
                conflicts.append(
                    RecordConflict(
                        domain=canonical_domain,
                        field_name=field_name,
                        observed_values=observed_values,
                        sources=all_sources,
                    )
                )

    return conflicts
