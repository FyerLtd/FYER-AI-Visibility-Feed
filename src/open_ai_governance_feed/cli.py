from __future__ import annotations

import argparse
from typing import Sequence

from . import __version__


def _print_version() -> int:
    print(f"Open AI Governance Feed {__version__}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="open_ai_governance_feed.cli",
        description="Open AI Governance Feed CLI.",
    )
    subparsers = parser.add_subparsers(dest="command")
    version_parser = subparsers.add_parser("version", help="Print the package version.")
    version_parser.set_defaults(func=_print_version)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not hasattr(args, "func"):
        parser.print_help()
        return 0

    return args.func()


if __name__ == "__main__":
    raise SystemExit(main())
