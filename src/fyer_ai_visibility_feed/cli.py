from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

from . import __version__
from .exporters import export_csv, export_json
from .integrity import write_integrity_files
from .loaders import load_json
from .seed_pipeline import build_manual_seed
from .source_registry import load_source_registry
from .validators import validate_record


def _print_version() -> int:
    print(f"FYER AI Visibility Feed {__version__}")
    return 0


def _write_feed(
    records,
    output_dir: Path,
) -> tuple[Path, Path]:
    """Write CSV and JSON feed files and return their paths."""

    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "feed.csv"
    json_path = output_dir / "feed.json"

    export_csv(list(records), csv_path)
    export_json(list(records), json_path)

    return csv_path, json_path


def _export_feed(
    input_path: Path,
    output_dir: Path,
) -> int:
    """Validate canonical records and export CSV and JSON feeds."""

    records = load_json(input_path)
    validation_errors: list[str] = []

    for index, record in enumerate(records, start=1):
        for error in validate_record(record):
            validation_errors.append(
                f"record {index} ({record.domain}): {error}"
            )

    if validation_errors:
        print("Validation failed:")

        for error in validation_errors:
            print(f"- {error}")

        return 1

    csv_path, json_path = _write_feed(records, output_dir)

    print(f"Exported {len(records)} record(s).")
    print(f"CSV: {csv_path}")
    print(f"JSON: {json_path}")

    return 0


def _build_seed_feed(
    seed_path: Path,
    registry_path: Path,
    output_dir: Path,
    source_commit: str,
) -> int:
    """Build canonical feeds and integrity metadata from governed seeds."""

    records = load_json(seed_path)
    policies = load_source_registry(registry_path)
    result = build_manual_seed(records, policies)

    if not result.succeeded:
        print("Seed build failed:")

        for error in result.errors:
            print(f"- {error}")

        return 1

    csv_path, json_path = _write_feed(result.records, output_dir)
    manifest_path, checksums_path = write_integrity_files(
        output_dir,
        result.records,
        result.conflicts,
        generated_at=datetime.now(timezone.utc),
        source_commit=source_commit,
    )

    print(f"Built {len(result.records)} canonical record(s).")
    print(f"Conflicts: {len(result.conflicts)}")
    print(f"CSV: {csv_path}")
    print(f"JSON: {json_path}")
    print(f"Manifest: {manifest_path}")
    print(f"Checksums: {checksums_path}")

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fyer_ai_visibility_feed.cli",
        description="FYER AI Visibility Feed CLI.",
    )

    subparsers = parser.add_subparsers(dest="command")

    version_parser = subparsers.add_parser(
        "version",
        help="Print the package version.",
    )
    version_parser.set_defaults(func=_print_version)

    export_parser = subparsers.add_parser(
        "export",
        help="Validate canonical JSON and export governance feeds.",
    )
    export_parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Path to the canonical JSON input file.",
    )
    export_parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory for generated feed files.",
    )
    export_parser.set_defaults(
        func=lambda args: _export_feed(
            args.input,
            args.output_dir,
        )
    )

    build_seed_parser = subparsers.add_parser(
        "build-seed",
        help="Build governed canonical feeds from manual seed data.",
    )
    build_seed_parser.add_argument(
        "--seed",
        type=Path,
        required=True,
        help="Path to the manual seed JSON file.",
    )
    build_seed_parser.add_argument(
        "--registry",
        type=Path,
        required=True,
        help="Path to the governed source registry JSON file.",
    )
    build_seed_parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory for generated feed files.",
    )
    build_seed_parser.add_argument(
        "--source-commit",
        default="unknown",
        help="Source commit recorded in the integrity manifest.",
    )
    build_seed_parser.set_defaults(
        func=lambda args: _build_seed_feed(
            args.seed,
            args.registry,
            args.output_dir,
            args.source_commit,
        )
    )

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not hasattr(args, "func"):
        parser.print_help()
        return 0

    if args.command == "version":
        return args.func()

    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
