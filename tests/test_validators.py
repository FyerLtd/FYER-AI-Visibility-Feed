from datetime import date

from open_ai_governance_feed.models import GovernanceRecord
from open_ai_governance_feed.validators import validate_record


def test_valid_record_passes_validation():
    record = GovernanceRecord(
        tool_name="Example AI",
        domain="example.ai",
        category="generative-ai",
        sources=["https://example.com/source"],
        risk_rating="unknown",
        last_seen=date(2026, 10, 31),
        notes="Test fixture only.",
    )

    assert validate_record(record) == []


def test_missing_source_is_rejected():
    record = GovernanceRecord(
        tool_name="Example AI",
        domain="example.ai",
        category="generative-ai",
        sources=[],
    )

    errors = validate_record(record)

    assert "at least one source is required" in errors


def test_invalid_source_url_is_rejected():
    record = GovernanceRecord(
        tool_name="Example AI",
        domain="example.ai",
        category="generative-ai",
        sources=["some directory somewhere"],
    )

    errors = validate_record(record)

    assert "sources must contain valid HTTP or HTTPS URLs" in errors


def test_invalid_domain_is_rejected():
    record = GovernanceRecord(
        tool_name="Example AI",
        domain="not a domain",
        category="generative-ai",
        sources=["https://example.com/source"],
    )

    errors = validate_record(record)

    assert "domain must be a valid hostname" in errors


def test_invalid_risk_rating_is_rejected():
    record = GovernanceRecord(
        tool_name="Example AI",
        domain="example.ai",
        category="generative-ai",
        sources=["https://example.com/source"],
        risk_rating="super-mega-dangerous",
    )

    errors = validate_record(record)

    assert "risk_rating must be one of: unknown, low, medium, high" in errors
