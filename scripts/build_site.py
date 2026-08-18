#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from njptr_lab.site_builder import build_site


REPO_ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the NJ Property Tax Relief static site")
    parser.add_argument("--base-url", default="https://example.invalid", help="Canonical public base URL")
    args = parser.parse_args()
    output = build_site(root=REPO_ROOT, base_url=args.base_url)
    print(f"Site built: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
