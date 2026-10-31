"""Generate integrity metadata for canonical feed artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Sequence

from . import __version__
from .models import GovernanceRecord, RecordConflict


ARTIFACT_NAMES = (
    "feed.csv",
    "feed.json",
)


def sha256_file(path: Path) -> str:
    """Return the SHA-256 digest of a file."""

    digest = hashlib.sha256()

    with path.open("rb") as artifact_file:
        for chunk in iter(lambda: artifact_file.read(65536), b""):
            digest.update(chunk)

    return digest.hexdigest()


def write_integrity_files(
    output_dir: Path,
    records: Sequence[GovernanceRecord],
    conflicts: Sequence[RecordConflict],
    *,
    generated_at: datetime,
    source_commit: str,
) -> tuple[Path, Path]:
    """Write a feed manifest and SHA-256 checksum file.

    The canonical feed files must already exist and be non-empty. Integrity
    metadata is generated only after both expected artifacts are present.
    """

    artifacts = []

    for artifact_name in ARTIFACT_NAMES:
        artifact_path = output_dir / artifact_name

        if not artifact_path.is_file():
            raise FileNotFoundError(
                f"required feed artifact is missing: {artifact_name}"
            )

        if artifact_path.stat().st_size == 0:
            raise ValueError(
                f"required feed artifact is empty: {artifact_name}"
            )

        artifacts.append(
            {
                "name": artifact_name,
                "sha256": sha256_file(artifact_path),
                "size_bytes": artifact_path.stat().st_size,
            }
        )

    manifest = {
        "feed_name": "FYER AI Visibility Feed",
        "schema_version": "1.0",
        "feed_version": __version__,
        "generated_at": generated_at.isoformat(),
        "source_commit": source_commit,
        "record_count": len(records),
        "conflict_count": len(conflicts),
        "licence": "MIT",
        "intended_use": (
            "Governance visibility and review; not an automatic allow or "
            "block recommendation."
        ),
        "artifacts": artifacts,
    }

    manifest_path = output_dir / "manifest.json"
    checksums_path = output_dir / "SHA256SUMS"

    with manifest_path.open("w", encoding="utf-8") as manifest_file:
        json.dump(
            manifest,
            manifest_file,
            indent=2,
            ensure_ascii=False,
        )
        manifest_file.write("\n")

    with checksums_path.open("w", encoding="utf-8") as checksums_file:
        for artifact in artifacts:
            checksums_file.write(
                f"{artifact['sha256']}  {artifact['name']}\n"
            )

        checksums_file.write(
            f"{sha256_file(manifest_path)}  {manifest_path.name}\n"
        )

    return manifest_path, checksums_path
