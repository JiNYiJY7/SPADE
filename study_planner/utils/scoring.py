from __future__ import annotations
from datetime import datetime
from ..models import Task


def priority_score(task: Task, now: datetime) -> float:
    """
    Higher score => higher priority.
    Factors:
    - Urgency: closer due date => higher
    - Importance: 1..5 weight
    - Workload: remaining time (hours)
    """
    hours_left = (task.due - now).total_seconds() / 3600.0

    if hours_left <= 0:
        urgency = 9999.0
    else:
        urgency = 1.0 / hours_left

    importance = float(task.importance)
    workload_hours = task.remaining_minutes / 60.0

    return urgency * 100.0 + importance * 10.0 + workload_hours
