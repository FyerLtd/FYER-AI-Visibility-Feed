from datetime import date

from fyer_ai_visibility_feed.models import SourcePolicy
from fyer_ai_visibility_feed.validators import (
    source_is_collection_eligible,
    validate_source_policy,
)


def test_new_source_defaults_to_pending_review():
    policy = SourcePolicy(
        name="Example Directory",
        homepage_url="https://directory.example/",
    )

    assert policy.collection_status == "pending-review"
    assert policy.collection_method == "manual"


def test_pending_review_source_is_not_collection_eligible():
    policy = SourcePolicy(
        name="Example Directory",
        homepage_url="https://directory.example/",
    )

    assert source_is_collection_eligible(policy) is False


def test_prohibited_source_is_not_collection_eligible():
    policy = SourcePolicy(
        name="Example Directory",
        homepage_url="https://directory.example/",
        collection_status="prohibited",
    )

    assert source_is_collection_eligible(policy) is False


def test_approved_manual_source_can_be_collection_eligible():
    policy = SourcePolicy(
        name="Example Directory",
        homepage_url="https://directory.example/",
        collection_status="approved",
        collection_method="manual",
        permitted_metadata=[
            "tool_name",
            "domain",
        ],
        reviewed_at=date(2026, 10, 31),
        reviewer="Test Reviewer",
    )

    assert validate_source_policy(policy) == []
    assert source_is_collection_eligible(policy) is True


def test_approved_source_requires_review_date():
    policy = SourcePolicy(
        name="Example Directory",
        homepage_url="https://directory.example/",
        collection_status="approved",
        collection_method="manual",
        permitted_metadata=["domain"],
        reviewer="Test Reviewer",
    )

    errors = validate_source_policy(policy)

    assert "approved sources require reviewed_at" in errors
    assert source_is_collection_eligible(policy) is False


def test_approved_source_requires_reviewer():
    policy = SourcePolicy(
        name="Example Directory",
        homepage_url="https://directory.example/",
        collection_status="approved",
        collection_method="manual",
        permitted_metadata=["domain"],
        reviewed_at=date(2026, 10, 31),
    )

    errors = validate_source_policy(policy)

    assert "approved sources require reviewer" in errors
    assert source_is_collection_eligible(policy) is False


def test_approved_source_requires_permitted_metadata():
    policy = SourcePolicy(
        name="Example Directory",
        homepage_url="https://directory.example/",
        collection_status="approved",
        collection_method="manual",
        reviewed_at=date(2026, 10, 31),
        reviewer="Test Reviewer",
    )

    errors = validate_source_policy(policy)

    assert "approved sources require permitted_metadata" in errors
    assert source_is_collection_eligible(policy) is False


def test_approved_html_source_requires_terms_url():
    policy = SourcePolicy(
        name="Example Directory",
        homepage_url="https://directory.example/",
        collection_status="approved",
        collection_method="html",
        robots_url="https://directory.example/robots.txt",
        permitted_metadata=["domain"],
        reviewed_at=date(2026, 10, 31),
        reviewer="Test Reviewer",
    )

    errors = validate_source_policy(policy)

    assert "approved automated sources require terms_url" in errors
    assert source_is_collection_eligible(policy) is False


def test_approved_html_source_requires_robots_url():
    policy = SourcePolicy(
        name="Example Directory",
        homepage_url="https://directory.example/",
        collection_status="approved",
        collection_method="html",
        terms_url="https://directory.example/terms",
        permitted_metadata=["domain"],
        reviewed_at=date(2026, 10, 31),
        reviewer="Test Reviewer",
    )

    errors = validate_source_policy(policy)

    assert "approved HTML sources require robots_url" in errors
    assert source_is_collection_eligible(policy) is False


def test_fully_reviewed_html_source_is_collection_eligible():
    policy = SourcePolicy(
        name="Example Directory",
        homepage_url="https://directory.example/",
        collection_status="approved",
        collection_method="html",
        terms_url="https://directory.example/terms",
        robots_url="https://directory.example/robots.txt",
        permitted_metadata=[
            "tool_name",
            "domain",
            "category",
        ],
        reviewed_at=date(2026, 10, 31),
        reviewer="Test Reviewer",
    )

    assert validate_source_policy(policy) == []
    assert source_is_collection_eligible(policy) is True


def test_unknown_collection_status_is_rejected():
    policy = SourcePolicy(
        name="Example Directory",
        homepage_url="https://directory.example/",
        collection_status="YOLO",
    )

    errors = validate_source_policy(policy)

    assert (
        "collection_status must be one of: "
        "pending-review, approved, prohibited"
        in errors
    )

    assert source_is_collection_eligible(policy) is False


def test_unknown_collection_method_is_rejected():
    policy = SourcePolicy(
        name="Example Directory",
        homepage_url="https://directory.example/",
        collection_method="magic-scraper",
    )

    errors = validate_source_policy(policy)

    assert (
        "collection_method must be one of: "
        "manual, api, html, feed"
        in errors
    )


def test_invalid_policy_url_is_rejected():
    policy = SourcePolicy(
        name="Example Directory",
        homepage_url="not-a-url",
    )

    errors = validate_source_policy(policy)

    assert (
        "homepage_url must be a valid HTTP or HTTPS URL"
        in errors
    )
