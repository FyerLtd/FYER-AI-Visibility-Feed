"""Conservative deduplication for governance records."""

from __future__ import annotations

from dataclasses import replace

from .models import GovernanceRecord
from .normalizers import normalize_domain


def deduplicate_records(
    records: list[GovernanceRecord],
) -> list[GovernanceRecord]:
    """Merge records sharing the same normalized hostname.

    Deduplication is intentionally conservative. Records are merged only
    when their normalized hostname is identical. Source provenance and
    structured evidence are preserved across merged observations.
    """

    deduplicated: dict[str, GovernanceRecord] = {}

    for record in records:
        canonical_domain = normalize_domain(record.domain)

        if canonical_domain not in deduplicated:
            deduplicated[canonical_domain] = replace(
                record,
                domain=canonical_domain,
                sources=list(dict.fromkeys(record.sources)),
                evidence=list(record.evidence),
            )
            continue

        existing = deduplicated[canonical_domain]

        merged_sources = list(
            dict.fromkeys(existing.sources + record.sources)
        )

        merged_evidence = list(existing.evidence)

        for evidence in record.evidence:
            if evidence not in merged_evidence:
                merged_evidence.append(evidence)

        # Keep the most recent observation date when both are available.
        last_seen_values = [
            value
            for value in (existing.last_seen, record.last_seen)
            if value is not None
        ]

        latest_last_seen = (
            max(last_seen_values)
            if last_seen_values
            else None
        )

        deduplicated[canonical_domain] = replace(
            existing,
            sources=merged_sources,
            evidence=merged_evidence,
            last_seen=latest_last_seen,
        )

    return list(deduplicated.values())
