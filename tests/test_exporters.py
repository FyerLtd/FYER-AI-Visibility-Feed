import csv
from datetime import date
from pathlib import Path

from open_ai_governance_feed.exporters import export_csv
from open_ai_governance_feed.models import GovernanceRecord


def make_record(
    *,
    name: str,
    domain: str,
    sources: list[str],
    last_seen: date | None = None,
) -> GovernanceRecord:
    return GovernanceRecord(
        tool_name=name,
        domain=domain,
        category="generative-ai",
        sources=sources,
        risk_rating="unknown",
        last_seen=last_seen,
        notes="Test fixture only.",
    )


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as csv_file:
        return list(csv.DictReader(csv_file))


def test_export_csv_creates_file(tmp_path):
    output = tmp_path / "feed.csv"

    records = [
        make_record(
            name="Example AI",
            domain="example.ai",
            sources=["https://directory.example/tool"],
        )
    ]

    export_csv(records, output)

    assert output.exists()


def test_export_csv_writes_expected_fields(tmp_path):
    output = tmp_path / "feed.csv"

    records = [
        make_record(
            name="Example AI",
            domain="example.ai",
            sources=["https://directory.example/tool"],
        )
    ]

    export_csv(records, output)

    rows = read_csv(output)

    assert rows[0]["tool_name"] == "Example AI"
    assert rows[0]["domain"] == "example.ai"
    assert rows[0]["category"] == "generative-ai"
    assert rows[0]["risk_rating"] == "unknown"


def test_export_csv_preserves_multiple_sources(tmp_path):
    output = tmp_path / "feed.csv"

    records = [
        make_record(
            name="Example AI",
            domain="example.ai",
            sources=[
                "https://directory-a.example/tool",
                "https://directory-b.example/tool",
            ],
        )
    ]

    export_csv(records, output)

    rows = read_csv(output)

    assert rows[0]["sources"] == (
        "https://directory-a.example/tool;"
        "https://directory-b.example/tool"
    )


def test_export_csv_formats_last_seen_as_iso_date(tmp_path):
    output = tmp_path / "feed.csv"

    records = [
        make_record(
            name="Example AI",
            domain="example.ai",
            sources=["https://directory.example/tool"],
            last_seen=date(2026, 10, 31),
        )
    ]

    export_csv(records, output)

    rows = read_csv(output)

    assert rows[0]["last_seen"] == "2026-10-31"


def test_export_csv_writes_multiple_records(tmp_path):
    output = tmp_path / "feed.csv"

    records = [
        make_record(
            name="Example AI",
            domain="example.ai",
            sources=["https://directory.example/example-ai"],
        ),
        make_record(
            name="Second AI",
            domain="second.example",
            sources=["https://directory.example/second-ai"],
        ),
    ]

    export_csv(records, output)

    rows = read_csv(output)

    assert len(rows) == 2
    assert rows[0]["domain"] == "example.ai"
    assert rows[1]["domain"] == "second.example"
