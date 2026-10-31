from pathlib import Path

from open_ai_governance_feed.loaders import load_json
from open_ai_governance_feed.seed_pipeline import build_manual_seed
from open_ai_governance_feed.source_registry import load_source_registry


REPO_ROOT = Path(__file__).resolve().parents[1]
SEED_PATH = REPO_ROOT / "data" / "manual-seed.json"
REGISTRY_PATH = REPO_ROOT / "data" / "sources.json"


def build_repository_seed():
    records = load_json(SEED_PATH)
    policies = load_source_registry(REGISTRY_PATH)

    return build_manual_seed(records, policies)


def test_repository_manual_seed_contains_three_records():
    records = load_json(SEED_PATH)

    assert len(records) == 3


def test_repository_manual_seed_build_succeeds():
    result = build_repository_seed()

    assert result.succeeded is True
    assert result.errors == ()


def test_repository_manual_seed_builds_expected_domains():
    result = build_repository_seed()

    assert [record.domain for record in result.records] == [
        "copilot.cloud.microsoft",
        "chatgpt.com",
        "claude.ai",
    ]


def test_repository_manual_seed_has_no_conflicts():
    result = build_repository_seed()

    assert result.conflicts == ()


def test_repository_manual_seed_preserves_governed_evidence():
    result = build_repository_seed()

    assert all(len(record.evidence) == 1 for record in result.records)
    assert all(
        record.evidence[0].source_name == "Manual Seed Dataset"
        for record in result.records
    )
    assert all(
        record.risk_rating == "unknown"
        for record in result.records
    )
