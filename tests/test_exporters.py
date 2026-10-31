import csv
import json
from datetime import date, datetime, timezone
from pathlib import Path

from open_ai_governance_feed.exporters import export_csv, export_json
from open_ai_governance_feed.models import (
    GovernanceRecord,
    SourceEvidence,
)


def make_record(
    *,
    name: str,
    domain: str,
    sources: list[str],
    last_seen: date | None = None,
    evidence: list[SourceEvidence] | None = None,
) -> GovernanceRecord:
    return GovernanceRecord(
        tool_name=name,
        domain=domain,
        category="generative-ai",
        sources=sources,
        risk_rating="unknown",
        last_seen=last_seen,
        notes="Test fixture only.",
        evidence=evidence or [],
    )


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as csv_file:
        return list(csv.DictReader(csv_file))


def read_json(path: Path):
    with path.open(
        "r",
        encoding="utf-8",
    ) as json_file:
        return json.load(json_file)


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


def test_export_json_creates_file(tmp_path):
    output = tmp_path / "feed.json"

    records = [
        make_record(
            name="Example AI",
            domain="example.ai",
            sources=["https://directory.example/tool"],
        )
    ]

    export_json(records, output)

    assert output.exists()


def test_export_json_writes_expected_fields(tmp_path):
    output = tmp_path / "feed.json"

    records = [
        make_record(
            name="Example AI",
            domain="example.ai",
            sources=["https://directory.example/tool"],
            last_seen=date(2026, 10, 31),
        )
    ]

    export_json(records, output)

    payload = read_json(output)

    assert len(payload) == 1
    assert payload[0]["tool_name"] == "Example AI"
    assert payload[0]["domain"] == "example.ai"
    assert payload[0]["category"] == "generative-ai"
    assert payload[0]["risk_rating"] == "unknown"
    assert payload[0]["last_seen"] == "2026-10-31"
    assert payload[0]["notes"] == "Test fixture only."


def test_export_json_preserves_sources_as_array(tmp_path):
    output = tmp_path / "feed.json"

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

    export_json(records, output)

    payload = read_json(output)

    assert payload[0]["sources"] == [
        "https://directory-a.example/tool",
        "https://directory-b.example/tool",
    ]


def test_export_json_preserves_structured_evidence(tmp_path):
    output = tmp_path / "feed.json"

    evidence = SourceEvidence(
        source_name="Directory A",
        source_url="https://directory-a.example/tool",
        observed_at=datetime(
            2026,
            10,
            31,
            9,
            30,
            tzinfo=timezone.utc,
        ),
    )

    records = [
        make_record(
            name="Example AI",
            domain="example.ai",
            sources=["https://directory-a.example/tool"],
            evidence=[evidence],
        )
    ]

    export_json(records, output)

    payload = read_json(output)

    assert payload[0]["evidence"] == [
        {
            "source_name": "Directory A",
            "source_url": "https://directory-a.example/tool",
            "observed_at": "2026-10-31T09:30:00+00:00",
        }
    ]


def test_export_json_writes_multiple_records(tmp_path):
    output = tmp_path / "feed.json"

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

    export_json(records, output)

    payload = read_json(output)

    assert len(payload) == 2
    assert payload[0]["domain"] == "example.ai"
    assert payload[1]["domain"] == "second.example"
