from datetime import date, datetime, timezone

from open_ai_governance_feed.models import (
    GovernanceRecord,
    SourceEvidence,
    SourcePolicy,
)
from open_ai_governance_feed.seed_pipeline import build_manual_seed


def make_policy(
    *,
    name: str = "Manual Seed Dataset",
    status: str = "approved",
) -> SourcePolicy:
    return SourcePolicy(
        name=name,
        homepage_url="https://source.example/",
        collection_status=status,
        collection_method="manual",
        permitted_metadata=[
            "tool_name",
            "domain",
            "category",
        ],
        reviewed_at=(
            date(2026, 10, 31)
            if status == "approved"
            else None
        ),
        reviewer=(
            "Test Reviewer"
            if status == "approved"
            else None
        ),
        notes="Test fixture only.",
    )


def make_evidence(
    *,
    source_name: str = "Manual Seed Dataset",
    source_url: str = "https://source.example/tool",
    minute: int = 0,
) -> SourceEvidence:
    return SourceEvidence(
        source_name=source_name,
        source_url=source_url,
        observed_at=datetime(
            2026,
            10,
            31,
            10,
            minute,
            tzinfo=timezone.utc,
        ),
    )


def make_record(
    *,
    name: str = "Example AI",
    domain: str = "example.ai",
    category: str = "generative-ai",
    source_url: str = "https://source.example/tool",
    evidence: list[SourceEvidence] | None = None,
) -> GovernanceRecord:
    return GovernanceRecord(
        tool_name=name,
        domain=domain,
        category=category,
        sources=[source_url],
        risk_rating="unknown",
        last_seen=date(2026, 10, 31),
        notes="Test fixture only.",
        evidence=(
            [make_evidence(source_url=source_url)]
            if evidence is None
            else evidence
        ),
    )


def test_pending_review_source_fails_closed():
    result = build_manual_seed(
        [make_record()],
        [make_policy(status="pending-review")],
    )

    assert result.succeeded is False
    assert result.records == ()
    assert result.conflicts == ()
    assert result.errors == (
        "record 1 (example.ai): source is not "
        "collection-eligible: Manual Seed Dataset",
    )


def test_unregistered_evidence_source_fails_closed():
    evidence = make_evidence(source_name="Unknown Directory")

    result = build_manual_seed(
        [make_record(evidence=[evidence])],
        [make_policy()],
    )

    assert result.succeeded is False
    assert result.records == ()
    assert result.errors == (
        "record 1 (example.ai): unregistered evidence source: "
        "Unknown Directory",
    )


def test_missing_structured_evidence_fails_closed():
    result = build_manual_seed(
        [make_record(evidence=[])],
        [make_policy()],
    )

    assert result.succeeded is False
    assert result.records == ()
    assert result.errors == (
        "record 1 (example.ai): structured source evidence "
        "is required",
    )


def test_approved_manual_source_builds_canonical_record():
    result = build_manual_seed(
        [make_record()],
        [make_policy()],
    )

    assert result.succeeded is True
    assert result.errors == ()
    assert len(result.records) == 1
    assert result.records[0].domain == "example.ai"
    assert result.conflicts == ()


def test_duplicate_observations_merge_and_preserve_evidence():
    first = make_record(
        domain="www.example.ai",
        source_url="https://source.example/first",
        evidence=[
            make_evidence(
                source_url="https://source.example/first",
                minute=0,
            )
        ],
    )
    second = make_record(
        domain="Example.AI.",
        source_url="https://source.example/second",
        evidence=[
            make_evidence(
                source_url="https://source.example/second",
                minute=5,
            )
        ],
    )

    result = build_manual_seed(
        [first, second],
        [make_policy()],
    )

    assert result.succeeded is True
    assert len(result.records) == 1
    assert result.records[0].domain == "example.ai"
    assert len(result.records[0].evidence) == 2
    assert result.records[0].sources == [
        "https://source.example/first",
        "https://source.example/second",
    ]


def test_conflicting_observations_are_surfaced():
    first = make_record(
        category="generative-ai",
        source_url="https://source.example/first",
        evidence=[
            make_evidence(
                source_url="https://source.example/first",
                minute=0,
            )
        ],
    )
    second = make_record(
        domain="www.example.ai",
        category="coding-assistant",
        source_url="https://source.example/second",
        evidence=[
            make_evidence(
                source_url="https://source.example/second",
                minute=5,
            )
        ],
    )

    result = build_manual_seed(
        [first, second],
        [make_policy()],
    )

    assert result.succeeded is True
    assert len(result.records) == 1
    assert len(result.conflicts) == 1
    assert result.conflicts[0].domain == "example.ai"
    assert result.conflicts[0].field_name == "category"
    assert result.conflicts[0].observed_values == (
        "generative-ai",
        "coding-assistant",
    )
