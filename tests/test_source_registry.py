import json
from datetime import date
from pathlib import Path

import pytest

from open_ai_governance_feed.models import SourcePolicy
from open_ai_governance_feed.source_registry import (
    collection_eligible_sources,
    load_source_registry,
    validate_source_registry,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "data" / "sources.json"


def write_registry(
    path: Path,
    payload,
) -> None:
    path.write_text(
        json.dumps(payload),
        encoding="utf-8",
    )


def test_repository_source_registry_loads():
    policies = load_source_registry(REGISTRY_PATH)

    assert len(policies) == 1
    assert policies[0].name == "Manual Seed Dataset"


def test_repository_source_defaults_remain_fail_closed():
    policies = load_source_registry(REGISTRY_PATH)

    policy = policies[0]

    assert policy.collection_status == "pending-review"
    assert policy.collection_method == "manual"
    assert policy.reviewed_at is None
    assert policy.reviewer is None


def test_repository_source_registry_is_valid():
    policies = load_source_registry(REGISTRY_PATH)

    assert validate_source_registry(policies) == []


def test_repository_source_is_not_collection_eligible():
    policies = load_source_registry(REGISTRY_PATH)

    assert collection_eligible_sources(policies) == []


def test_registry_loads_review_date(tmp_path):
    registry_path = tmp_path / "sources.json"

    write_registry(
        registry_path,
        [
            {
                "name": "Approved Manual Source",
                "homepage_url": "https://source.example/",
                "collection_status": "approved",
                "collection_method": "manual",
                "permitted_metadata": [
                    "tool_name",
                    "domain",
                ],
                "reviewed_at": "2026-10-31",
                "reviewer": "Test Reviewer",
                "notes": "Approved test fixture.",
            }
        ],
    )

    policies = load_source_registry(registry_path)

    assert policies[0].reviewed_at == date(2026, 10, 31)


def test_approved_valid_source_is_collection_eligible():
    approved = SourcePolicy(
        name="Approved Manual Source",
        homepage_url="https://source.example/",
        collection_status="approved",
        collection_method="manual",
        permitted_metadata=[
            "tool_name",
            "domain",
        ],
        reviewed_at=date(2026, 10, 31),
        reviewer="Test Reviewer",
    )

    pending = SourcePolicy(
        name="Pending Source",
        homepage_url="https://pending.example/",
    )

    eligible = collection_eligible_sources(
        [
            pending,
            approved,
        ]
    )

    assert eligible == [approved]


def test_duplicate_source_names_are_rejected():
    policies = [
        SourcePolicy(
            name="Example Directory",
            homepage_url="https://directory-a.example/",
        ),
        SourcePolicy(
            name=" example directory ",
            homepage_url="https://directory-b.example/",
        ),
    ]

    errors = validate_source_registry(policies)

    assert errors == [
        "source 2 has duplicate name:  example directory "
    ]


def test_registry_must_contain_json_array(tmp_path):
    registry_path = tmp_path / "sources.json"

    write_registry(
        registry_path,
        {
            "name": "Not an array",
        },
    )

    with pytest.raises(
        ValueError,
        match="source registry must contain a JSON array",
    ):
        load_source_registry(registry_path)


def test_registry_items_must_be_objects(tmp_path):
    registry_path = tmp_path / "sources.json"

    write_registry(
        registry_path,
        [
            "not an object",
        ],
    )

    with pytest.raises(
        ValueError,
        match="source registry item 1 must be an object",
    ):
        load_source_registry(registry_path)
