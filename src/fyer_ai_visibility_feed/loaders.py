"""Load canonical governance records."""

from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path

from .models import GovernanceRecord, SourceEvidence


def load_json(
    input_path: Path,
) -> list[GovernanceRecord]:
    """Load governance records from canonical JSON."""

    with input_path.open(
        "r",
        encoding="utf-8",
    ) as json_file:
        payload = json.load(json_file)

    records: list[GovernanceRecord] = []

    for item in payload:
        evidence = [
            SourceEvidence(
                source_name=evidence_item["source_name"],
                source_url=evidence_item["source_url"],
                observed_at=datetime.fromisoformat(
                    evidence_item["observed_at"]
                ),
            )
            for evidence_item in item.get("evidence", [])
        ]

        last_seen_value = item.get("last_seen")

        records.append(
            GovernanceRecord(
                tool_name=item["tool_name"],
                domain=item["domain"],
                category=item["category"],
                sources=list(item.get("sources", [])),
                risk_rating=item.get("risk_rating", "unknown"),
                last_seen=(
                    date.fromisoformat(last_seen_value)
                    if last_seen_value
                    else None
                ),
                notes=item.get("notes", ""),
                evidence=evidence,
            )
        )

    return records
