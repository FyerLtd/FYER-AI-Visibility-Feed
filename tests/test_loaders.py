from datetime import date, datetime, timezone

from open_ai_governance_feed.exporters import export_json
from open_ai_governance_feed.loaders import load_json
from open_ai_governance_feed.models import (
    GovernanceRecord,
    SourceEvidence,
)


def make_record() -> GovernanceRecord:
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

    return GovernanceRecord(
        tool_name="Example AI",
        domain="example.ai",
        category="generative-ai",
        sources=[
            "https://directory-a.example/tool",
            "https://directory-b.example/tool",
        ],
        risk_rating="unknown",
        last_seen=date(2026, 10, 31),
        notes="Test fixture only.",
        evidence=[evidence],
    )


def test_load_json_restores_governance_record(tmp_path):
    output = tmp_path / "feed.json"

    original = make_record()

    export_json([original], output)
    loaded = load_json(output)

    assert len(loaded) == 1
    assert loaded[0] == original


def test_load_json_restores_date_type(tmp_path):
    output = tmp_path / "feed.json"

    export_json([make_record()], output)
    loaded = load_json(output)

    assert loaded[0].last_seen == date(2026, 10, 31)
    assert isinstance(loaded[0].last_seen, date)


def test_load_json_restores_structured_evidence(tmp_path):
    output = tmp_path / "feed.json"

    export_json([make_record()], output)
    loaded = load_json(output)

    assert len(loaded[0].evidence) == 1

    evidence = loaded[0].evidence[0]

    assert evidence.source_name == "Directory A"
    assert evidence.source_url == "https://directory-a.example/tool"
    assert evidence.observed_at == datetime(
        2026,
        10,
        31,
        9,
        30,
        tzinfo=timezone.utc,
    )


def test_load_json_preserves_multiple_sources(tmp_path):
    output = tmp_path / "feed.json"

    export_json([make_record()], output)
    loaded = load_json(output)

    assert loaded[0].sources == [
        "https://directory-a.example/tool",
        "https://directory-b.example/tool",
    ]


def test_json_round_trip_preserves_complete_record(tmp_path):
    output = tmp_path / "feed.json"

    original_records = [
        make_record(),
    ]

    export_json(original_records, output)
    loaded_records = load_json(output)

    assert loaded_records == original_records
