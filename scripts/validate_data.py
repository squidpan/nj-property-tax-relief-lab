#!/usr/bin/env python3
from pathlib import Path

from njptr_lab.validator import has_errors, validate_repository


REPO_ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    issues = validate_repository(REPO_ROOT)
    if not issues:
        print("Validation passed: 0 issues")
        return 0
    for issue in issues:
        print(f"{issue.severity}: {issue.code}: {issue.message}")
    return 1 if has_errors(issues) else 0


if __name__ == "__main__":
    raise SystemExit(main())
