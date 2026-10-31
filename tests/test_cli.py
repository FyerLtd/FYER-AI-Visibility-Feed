import json
import os
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"


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
            "open_ai_governance_feed.cli",
            *args,
        ],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )


def write_canonical_json(
    path: Path,
    *,
    domain: str = "example.ai",
    source_name: str = "Example Directory",
) -> None:
    payload = [
        {
            "tool_name": "Example AI",
            "domain": domain,
            "category": "generative-ai",
            "sources": [
                "https://directory.example/tool",
            ],
            "risk_rating": "unknown",
            "last_seen": "2026-10-31",
            "notes": "Test fixture only.",
            "evidence": [
                {
                    "source_name": source_name,
                    "source_url": "https://directory.example/tool",
                    "observed_at": "2026-10-31T09:30:00+00:00",
                }
            ],
        }
    ]

    path.write_text(
        json.dumps(payload),
        encoding="utf-8",
    )


def test_cli_help_returns_zero() -> None:
    result = run_cli("--help")

    assert result.returncode == 0
    assert "usage:" in result.stdout.lower()


def test_cli_version_returns_zero() -> None:
    result = run_cli("version")

    assert result.returncode == 0


def test_cli_version_output() -> None:
    result = run_cli("version")

    assert "Open AI Governance Feed 0.1.0" in result.stdout


def test_cli_export_returns_zero_for_valid_input(tmp_path) -> None:
    input_path = tmp_path / "canonical.json"
    output_dir = tmp_path / "outputs"

    write_canonical_json(input_path)

    result = run_cli(
        "export",
        "--input",
        str(input_path),
        "--output-dir",
        str(output_dir),
    )

    assert result.returncode == 0
    assert "Exported 1 record(s)." in result.stdout


def test_cli_export_creates_csv_and_json(tmp_path) -> None:
    input_path = tmp_path / "canonical.json"
    output_dir = tmp_path / "outputs"

    write_canonical_json(input_path)

    result = run_cli(
        "export",
        "--input",
        str(input_path),
        "--output-dir",
        str(output_dir),
    )

    assert result.returncode == 0
    assert (output_dir / "feed.csv").exists()
    assert (output_dir / "feed.json").exists()


def test_cli_exported_json_preserves_evidence(tmp_path) -> None:
    input_path = tmp_path / "canonical.json"
    output_dir = tmp_path / "outputs"

    write_canonical_json(input_path)

    result = run_cli(
        "export",
        "--input",
        str(input_path),
        "--output-dir",
        str(output_dir),
    )

    assert result.returncode == 0

    exported = json.loads(
        (output_dir / "feed.json").read_text(
            encoding="utf-8",
        )
    )

    assert exported[0]["evidence"][0]["source_name"] == (
        "Example Directory"
    )
    assert exported[0]["evidence"][0]["source_url"] == (
        "https://directory.example/tool"
    )
    assert exported[0]["evidence"][0]["observed_at"] == (
        "2026-10-31T09:30:00+00:00"
    )


def test_cli_export_rejects_invalid_governance_record(
    tmp_path,
) -> None:
    input_path = tmp_path / "canonical.json"
    output_dir = tmp_path / "outputs"

    write_canonical_json(
        input_path,
        domain="not a domain",
    )

    result = run_cli(
        "export",
        "--input",
        str(input_path),
        "--output-dir",
        str(output_dir),
    )

    assert result.returncode == 1
    assert "Validation failed:" in result.stdout
    assert "domain must be a valid hostname" in result.stdout


def test_cli_invalid_input_creates_no_feed_files(
    tmp_path,
) -> None:
    input_path = tmp_path / "canonical.json"
    output_dir = tmp_path / "outputs"

    write_canonical_json(
        input_path,
        domain="not a domain",
    )

    result = run_cli(
        "export",
        "--input",
        str(input_path),
        "--output-dir",
        str(output_dir),
    )

    assert result.returncode == 1
    assert not (output_dir / "feed.csv").exists()
    assert not (output_dir / "feed.json").exists()
