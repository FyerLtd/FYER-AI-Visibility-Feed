from datetime import date

from open_ai_governance_feed.dedupe import deduplicate_records
from open_ai_governance_feed.models import GovernanceRecord


def make_record(
    *,
    name: str,
    domain: str,
    source: str,
    last_seen: date | None = None,
) -> GovernanceRecord:
    return GovernanceRecord(
        tool_name=name,
        domain=domain,
        category="generative-ai",
        sources=[source],
        risk_rating="unknown",
        last_seen=last_seen,
        notes="Test fixture only.",
    )


def test_same_normalized_domain_is_merged():
    records = [
        make_record(
            name="Example AI",
            domain="www.example.ai",
            source="https://directory-a.example/tool",
        ),
        make_record(
            name="Example AI",
            domain="Example.AI.",
            source="https://directory-b.example/tool",
        ),
    ]

    result = deduplicate_records(records)

    assert len(result) == 1
    assert result[0].domain == "example.ai"


def test_sources_are_preserved_when_records_merge():
    records = [
        make_record(
            name="Example AI",
            domain="example.ai",
            source="https://directory-a.example/tool",
        ),
        make_record(
            name="Example AI",
            domain="www.example.ai",
            source="https://directory-b.example/tool",
        ),
    ]

    result = deduplicate_records(records)

    assert result[0].sources == [
        "https://directory-a.example/tool",
        "https://directory-b.example/tool",
    ]


def test_duplicate_sources_are_not_repeated():
    records = [
        make_record(
            name="Example AI",
            domain="example.ai",
            source="https://directory-a.example/tool",
        ),
        make_record(
            name="Example AI",
            domain="www.example.ai",
            source="https://directory-a.example/tool",
        ),
    ]

    result = deduplicate_records(records)

    assert result[0].sources == [
        "https://directory-a.example/tool",
    ]


def test_most_recent_last_seen_is_preserved():
    records = [
        make_record(
            name="Example AI",
            domain="example.ai",
            source="https://directory-a.example/tool",
            last_seen=date(2026, 10, 20),
        ),
        make_record(
            name="Example AI",
            domain="www.example.ai",
            source="https://directory-b.example/tool",
            last_seen=date(2026, 10, 31),
        ),
    ]

    result = deduplicate_records(records)

    assert result[0].last_seen == date(2026, 10, 31)


def test_different_subdomains_are_not_merged():
    records = [
        make_record(
            name="Example AI",
            domain="chat.example.ai",
            source="https://directory-a.example/tool",
        ),
        make_record(
            name="Example AI",
            domain="api.example.ai",
            source="https://directory-b.example/tool",
        ),
    ]

    result = deduplicate_records(records)

    assert len(result) == 2


def test_similar_names_with_different_domains_are_not_merged():
    records = [
        make_record(
            name="Amazing AI",
            domain="amazing-ai.com",
            source="https://directory-a.example/tool",
        ),
        make_record(
            name="AmazingAI",
            domain="amazingai.com",
            source="https://directory-b.example/tool",
        ),
    ]

    result = deduplicate_records(records)

    assert len(result) == 2
