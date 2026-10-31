from open_ai_governance_feed.conflicts import detect_conflicts
from open_ai_governance_feed.models import GovernanceRecord


def make_record(
    *,
    name: str = "Magic AI",
    domain: str = "magic.ai",
    category: str = "generative-ai",
    risk_rating: str = "unknown",
    source: str,
) -> GovernanceRecord:
    return GovernanceRecord(
        tool_name=name,
        domain=domain,
        category=category,
        sources=[source],
        risk_rating=risk_rating,
        notes="Test fixture only.",
    )


def test_category_disagreement_creates_conflict():
    records = [
        make_record(
            category="generative-ai",
            source="https://directory-a.example/tool",
        ),
        make_record(
            domain="www.magic.ai",
            category="coding-assistant",
            source="https://directory-b.example/tool",
        ),
    ]

    conflicts = detect_conflicts(records)

    assert len(conflicts) == 1
    assert conflicts[0].domain == "magic.ai"
    assert conflicts[0].field_name == "category"
    assert conflicts[0].observed_values == (
        "generative-ai",
        "coding-assistant",
    )


def test_conflict_preserves_all_sources():
    records = [
        make_record(
            category="generative-ai",
            source="https://directory-a.example/tool",
        ),
        make_record(
            category="coding-assistant",
            source="https://directory-b.example/tool",
        ),
    ]

    conflicts = detect_conflicts(records)

    assert conflicts[0].sources == (
        "https://directory-a.example/tool",
        "https://directory-b.example/tool",
    )


def test_multiple_disputed_fields_create_separate_conflicts():
    records = [
        make_record(
            name="MagicAI",
            category="generative-ai",
            risk_rating="unknown",
            source="https://directory-a.example/tool",
        ),
        make_record(
            name="Magic AI",
            category="coding-assistant",
            risk_rating="medium",
            source="https://directory-b.example/tool",
        ),
    ]

    conflicts = detect_conflicts(records)

    assert {conflict.field_name for conflict in conflicts} == {
        "tool_name",
        "category",
        "risk_rating",
    }


def test_identical_observations_do_not_create_conflict():
    records = [
        make_record(
            source="https://directory-a.example/tool",
        ),
        make_record(
            domain="WWW.Magic.AI.",
            source="https://directory-b.example/tool",
        ),
    ]

    assert detect_conflicts(records) == []


def test_different_domains_are_not_compared():
    records = [
        make_record(
            domain="magic-ai.com",
            category="generative-ai",
            source="https://directory-a.example/tool",
        ),
        make_record(
            domain="magicai.com",
            category="coding-assistant",
            source="https://directory-b.example/tool",
        ),
    ]

    assert detect_conflicts(records) == []
