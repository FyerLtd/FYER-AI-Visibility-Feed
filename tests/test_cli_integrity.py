import json
import os
import subprocess
import sys
from pathlib import Path

from fyer_ai_visibility_feed.integrity import sha256_file


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
SEED_PATH = REPO_ROOT / "data" / "manual-seed.json"
REGISTRY_PATH = REPO_ROOT / "data" / "sources.json"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = (
        str(SRC_ROOT)
        if not pythonpath
        else str(SRC_ROOT) + os.pathsep + pythonpath
    )

    return subprocess.run(
        [
            sys.executable,
            "-m",
            "fyer_ai_visibility_feed.cli",
            *args,
        ],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )


def test_cli_build_seed_creates_integrity_files(tmp_path):
    output_dir = tmp_path / "outputs"

    result = run_cli(
        "build-seed",
        "--seed",
        str(SEED_PATH),
        "--registry",
        str(REGISTRY_PATH),
        "--output-dir",
        str(output_dir),
        "--source-commit",
        "test-commit-123",
    )

    assert result.returncode == 0
    assert (output_dir / "manifest.json").exists()
    assert (output_dir / "SHA256SUMS").exists()
    assert "Manifest:" in result.stdout
    assert "Checksums:" in result.stdout


def test_cli_manifest_records_repository_build_metadata(tmp_path):
    output_dir = tmp_path / "outputs"

    result = run_cli(
        "build-seed",
        "--seed",
        str(SEED_PATH),
        "--registry",
        str(REGISTRY_PATH),
        "--output-dir",
        str(output_dir),
        "--source-commit",
        "test-commit-123",
    )

    assert result.returncode == 0

    manifest = json.loads(
        (output_dir / "manifest.json").read_text(encoding="utf-8")
    )

    assert manifest["source_commit"] == "test-commit-123"
    assert manifest["record_count"] == 3
    assert manifest["conflict_count"] == 0
    assert manifest["feed_name"] == "FYER AI Visibility Feed"


def test_cli_checksums_verify_all_integrity_artifacts(tmp_path):
    output_dir = tmp_path / "outputs"

    result = run_cli(
        "build-seed",
        "--seed",
        str(SEED_PATH),
        "--registry",
        str(REGISTRY_PATH),
        "--output-dir",
        str(output_dir),
        "--source-commit",
        "test-commit-123",
    )

    assert result.returncode == 0

    checksums = (output_dir / "SHA256SUMS").read_text(
        encoding="utf-8"
    )

    for name in ("feed.csv", "feed.json", "manifest.json"):
        expected = f"{sha256_file(output_dir / name)}  {name}"
        assert expected in checksums
