from __future__ import annotations
from datetime import datetime
from typing import Any


def parse_iso(iso_string: str) -> datetime:
    # Accepts ISO8601 without timezone. Example: "2026-01-05T23:59:00"
    return datetime.fromisoformat(iso_string)


def now_local() -> datetime:
    return datetime.now()


def as_minutes(delta_seconds: float) -> int:
    return int(delta_seconds // 60)
