"""Portable console configuration for Unicode CLI output."""

from __future__ import annotations

import sys


def configure_utf8_stdio():
    """Use UTF-8 for redirected and interactive output when supported."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            continue
        try:
            reconfigure(encoding="utf-8", errors="replace")
        except (OSError, ValueError):
            pass
