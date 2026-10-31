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


def test_cli_version_returns_zero() -> None
