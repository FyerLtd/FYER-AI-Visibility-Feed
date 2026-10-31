import os
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = str(SRC_ROOT) if not pythonpath else str(SRC_ROOT) + os.pathsep + pythonpath
    return subprocess.run(
        [sys.executable, "-m", "open_ai_governance_feed.cli", *args],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
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
