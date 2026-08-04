#!/usr/bin/env python3
"""PyInstaller entrypoint for the standalone CLI."""

from readme_architect.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
