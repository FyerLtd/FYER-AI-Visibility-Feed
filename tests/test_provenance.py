from datetime import datetime, timezone

from fyer_ai_visibility_feed.models import (
    GovernanceRecord,
    SourceEvidence,
)
from fyer_ai_visibility_feed.validators import validate_record


def make_record(
    evidence: list[SourceEvidence],
) -> GovernanceRecord:
    return GovernanceRecord(
        tool_name="Example AI",
        domain="example.ai",
        category="generative-ai",
        sources=["https://directory.example/tool"],
        risk_rating="unknown",
        notes="Test fixture only.",
        evidence=evidence,
    )


def test_valid_structured_evidence_passes_validation():
    evidence = SourceEvidence(
        source_name="Example Directory",
        source_url="https://directory.example/tool",
        observed_at=datetime(
            2026,
            10,
            31,
            8,
            0,
            tzinfo=timezone.utc,
        ),
    )

    record = make_record([evidence])

    assert validate_record(record) == []


def test_evidence_preserves_source_identity():
    evidence = SourceEvidence(
        source_name="Directory A",
        source_url="https://directory-a.example/tool",
        observed_at=datetime(
            2026,
            10,
            31,
            8,
            0,
            tzinfo=timezone.utc,
        ),
    )

    assert evidence.source_name == "Directory A"
    assert evidence.source_url == "https://directory-a.example/tool"


def test_missing_evidence_source_name_is_rejected():
    evidence = SourceEvidence(
        source_name="",
        source_url="https://directory.example/tool",
        observed_at=datetime(
            2026,
            10,
            31,
            8,
            0,
            tzinfo=timezone.utc,
        ),
    )

    errors = validate_record(make_record([evidence]))

    assert "evidence source_name is required" in errors


def test_invalid_evidence_source_url_is_rejected():
    evidence = SourceEvidence(
        source_name="Example Directory",
        source_url="not-a-url",
        observed_at=datetime(
            2026,
            10,
            31,
            8,
            0,
            tzinfo=timezone.utc,
        ),
    )

    errors = validate_record(make_record([evidence]))

    assert (
        "evidence source_url must be a valid HTTP or HTTPS URL"
        in errors
    )


def test_multiple_evidence_items_are_preserved():
    first = SourceEvidence(
        source_name="Directory A",
        source_url="https://directory-a.example/tool",
        observed_at=datetime(
            2026,
            10,
            31,
            8,
            0,
            tzinfo=timezone.utc,
        ),
    )

    second = SourceEvidence(
        source_name="Directory B",
        source_url="https://directory-b.example/tool",
        observed_at=datetime(
            2026,
            10,
            31,
            8,
            5,
            tzinfo=timezone.utc,
        ),
    )

    record = make_record([first, second])

    assert record.evidence == [first, second]
