"""Export canonical governance records."""

from __future__ import annotations

import csv
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
