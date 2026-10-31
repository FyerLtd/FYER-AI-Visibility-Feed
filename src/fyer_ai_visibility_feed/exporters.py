"""Export canonical governance records."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from .models import GovernanceRecord


CSV_FIELDS = (
    "tool_name",
    "domain",
    "category",
    "sources",
    "risk_rating",
    "last_seen",
    "notes",
)


def export_csv(
    records: list[GovernanceRecord],
    output_path: Path,
) -> None:
    """Write canonical governance records to a CSV file."""

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=CSV_FIELDS,
        )

        writer.writeheader()

        for record in records:
            writer.writerow(
                {
                    "tool_name": record.tool_name,
                    "domain": record.domain,
                    "category": record.category,
                    "sources": ";".join(record.sources),
                    "risk_rating": record.risk_rating,
                    "last_seen": (
                        record.last_seen.isoformat()
                        if record.last_seen is not None
                        else ""
                    ),
                    "notes": record.notes,
                }
            )


def export_json(
    records: list[GovernanceRecord],
    output_path: Path,
) -> None:
    """Write canonical governance records with provenance to JSON."""

    output_path.parent.mkdir(parents=True, exist_ok=True)

    payload = []

    for record in records:
        payload.append(
            {
                "tool_name": record.tool_name,
                "domain": record.domain,
                "category": record.category,
                "sources": list(record.sources),
                "risk_rating": record.risk_rating,
                "last_seen": (
                    record.last_seen.isoformat()
                    if record.last_seen is not None
                    else None
                ),
                "notes": record.notes,
                "evidence": [
                    {
                        "source_name": evidence.source_name,
                        "source_url": evidence.source_url,
                        "observed_at": evidence.observed_at.isoformat(),
                    }
                    for evidence in record.evidence
                ],
            }
        )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as json_file:
        json.dump(
            payload,
            json_file,
            indent=2,
            ensure_ascii=False,
        )

        json_file.write("\n")
