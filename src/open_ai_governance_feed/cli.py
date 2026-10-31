from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from . import __version__
from .exporters import export_csv, export_json
from .loaders import load_json
from .validators import validate_record


def _print_version() -> int:
    print(f"Open AI Governance Feed {__version__}")
    return 0


def _export_feed(
    input_path: Path,
    output_dir: Path,
) -> int:
    """Validate canonical records and export CSV and JSON feeds."""

    records = load_json(input_path)

    validation_errors: list[str] = []

    for index, record in enumerate(records, start=1):
        errors = validate_record(record)

        for error in errors:
            validation_errors.append(
                f"record {index} ({record.domain}): {error}"
            )

    if validation_errors:
        print("Validation failed:")

        for error in validation_errors:
            print(f"- {error}")

        return 1

    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "feed.csv"
    json_path = output_dir / "feed.json"

    export_csv(records, csv_path)
    export_json(records, json_path)

    print(f"Exported {len(records)} record(s).")
    print(f"CSV: {csv_path}")
    print(f"JSON: {json_path}")

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="open_ai_governance_feed.cli",
        description="Open AI Governance Feed CLI.",
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
