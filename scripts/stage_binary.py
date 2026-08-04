#!/usr/bin/env python3
"""Copy a PyInstaller binary into a stable release filename."""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    source = Path(args.source)
    output = Path(args.output)
    if not source.is_file():
        parser.error(f"binary not found: {source}")
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, output)
    if os.name != "nt":
        output.chmod(output.stat().st_mode | 0o111)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
