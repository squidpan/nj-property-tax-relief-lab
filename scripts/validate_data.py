#!/usr/bin/env python3
from njptr_lab.validator import has_errors, validate_repository


def main() -> int:
    issues = validate_repository()
    if not issues:
        print("Validation passed: 0 issues")
        return 0
    for issue in issues:
        print(f"{issue.severity}: {issue.code}: {issue.message}")
    return 1 if has_errors(issues) else 0


if __name__ == "__main__":
    raise SystemExit(main())
