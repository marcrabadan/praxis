"""Placeholder validation script.

Replace this with deterministic checks for this skill's output.

Exit codes:
- 0: all checks passed
- 1: one or more checks failed
- 2: invalid arguments or unreadable input
"""

from __future__ import annotations

import argparse
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate this skill's output.")
    parser.add_argument("path", help="Path to file or directory to validate.")
    args = parser.parse_args()

    print(f"TODO: validate {args.path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
