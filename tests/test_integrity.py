import hashlib
import json
from datetime import date, datetime, timezone

import pytest

from fyer_ai_visibility_feed.integrity import (
    sha256_file,
    write_integrity_files,
)
from fyer_ai_visibility_feed.models import GovernanceRecord


def make_record() -> GovernanceRecord:
    return GovernanceRecord(
        tool_name="Example AI",
        domain="example.ai",
        category="general-purpose-ai",
        sources=["https://example.ai/product"],
        risk_rating="unknown",
        last_seen=date(2026, 10, 31),
        notes="Test fixture only.",
    )


def write_feed_files(output_dir) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "feed.csv").write_text(
        "tool_name,domain\nExample AI,example.ai\n",
        encoding="utf-8",
    )
    (output_dir / "feed.json").write_text(
        '[{"tool_name":"Example AI","domain":"example.ai"}]\n',
        encoding="utf-8",
    )


def test_sha256_file_returns_expected_digest(tmp_path):
    artifact = tmp_path / "artifact.txt"
    artifact.write_bytes(b"FYER AI Visibility Feed\n")

    expected = hashlib.sha256(
        b"FYER AI Visibility Feed\n"
    ).hexdigest()

    assert sha256_file(artifact) == expected


def test_integrity_files_contain_expected_metadata(tmp_path):
    output_dir = tmp_path / "outputs"
    write_feed_files(output_dir)

    generated_at = datetime(
        2026,
        10,
        31,
        14,
        0,
        tzinfo=timezone.utc,
    )

    manifest_path, checksums_path = write_integrity_files(
        output_dir,
        [make_record()],
        [],
        generated_at=generated_at,
        source_commit="abc123",
    )

    manifest = json.loads(
        manifest_path.read_text(encoding="utf-8")
    )

    assert manifest["feed_name"] == "FYER AI Visibility Feed"
    assert manifest["schema_version"] == "1.0"
    assert manifest["feed_version"] == "0.1.0"
    assert manifest["generated_at"] == (
        "2026-10-31T14:00:00+00:00"
    )
    assert manifest["source_commit"] == "abc123"
    assert manifest["record_count"] == 1
    assert manifest["conflict_count"] == 0
    assert manifest["licence"] == "MIT"
    assert checksums_path.exists()


def test_manifest_records_artifact_digests_and_sizes(tmp_path):
    output_dir = tmp_path / "outputs"
    write_feed_files(output_dir)

    manifest_path, _ = write_integrity_files(
        output_dir,
        [make_record()],
        [],
        generated_at=datetime(
            2026,
            10,
            31,
            14,
            0,
            tzinfo=timezone.utc,
        ),
        source_commit="abc123",
    )

    manifest = json.loads(
        manifest_path.read_text(encoding="utf-8")
    )
    artifacts = {
        item["name"]: item
        for item in manifest["artifacts"]
    }

    for name in ("feed.csv", "feed.json"):
        path = output_dir / name
        assert artifacts[name]["sha256"] == sha256_file(path)
        assert artifacts[name]["size_bytes"] == path.stat().st_size


def test_checksums_cover_feed_files_and_manifest(tmp_path):
    output_dir = tmp_path / "outputs"
    write_feed_files(output_dir)

    manifest_path, checksums_path = write_integrity_files(
        output_dir,
        [make_record()],
        [],
        generated_at=datetime(
            2026,
            10,
            31,
            14,
            0,
            tzinfo=timezone.utc,
        ),
        source_commit="abc123",
    )

    checksums = checksums_path.read_text(encoding="utf-8")

    assert f"{sha256_file(output_dir / 'feed.csv')}  feed.csv" in checksums
    assert f"{sha256_file(output_dir / 'feed.json')}  feed.json" in checksums
    assert f"{sha256_file(manifest_path)}  manifest.json" in checksums


def test_missing_or_empty_feed_artifacts_fail_closed(tmp_path):
    output_dir = tmp_path / "outputs"
    output_dir.mkdir()
    (output_dir / "feed.csv").write_text("", encoding="utf-8")

    with pytest.raises(
        ValueError,
        match="required feed artifact is empty: feed.csv",
    ):
        write_integrity_files(
            output_dir,
            [make_record()],
            [],
            generated_at=datetime.now(timezone.utc),
            source_commit="abc123",
        )

    (output_dir / "feed.csv").write_text(
        "tool_name,domain\n",
        encoding="utf-8",
    )

    with pytest.raises(
        FileNotFoundError,
        match="required feed artifact is missing: feed.json",
    ):
        write_integrity_files(
            output_dir,
            [make_record()],
            [],
            generated_at=datetime.now(timezone.utc),
            source_commit="abc123",
        )
