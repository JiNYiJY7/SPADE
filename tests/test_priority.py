"""
Unit Test: Task Priority Scoring

Purpose:
- Verify that tasks with closer deadlines are scored higher than tasks with far deadlines.
- Ensures that the priority_score function correctly accounts for urgency.
"""

from datetime import datetime
from study_planner.models import Task
from study_planner.utils.scoring import priority_score


def test_priority_deadline_closer_higher():
    """
    Test that a task with a deadline closer to the current time
    receives a higher priority score than a task with a farther deadline.

    Why:
    - Core part of task scheduling logic.
    - Validates that urgency (time until due) is correctly factored into priority.
    """
    # Reference current time for consistent test results
    reference_time = datetime.fromisoformat("2026-01-02T10:00:00")

    # Task with a near deadline (2 hours away)
    task_near_deadline = Task(
        id="1",
        title="Close Deadline Task",
        due=datetime.fromisoformat("2026-01-02T12:00:00"),
        estimated_minutes=60,
        remaining_minutes=60,
        importance=3
    )

    # Task with a far deadline (3 days away)
    task_far_deadline = Task(
        id="2",
        title="Far Deadline Task",
        due=datetime.fromisoformat("2026-01-05T12:00:00"),
        estimated_minutes=60,
        remaining_minutes=60,
        importance=3
    )

    # Assertion: closer deadline should have higher priority
    assert priority_score(task_near_deadline, reference_time) > priority_score(
        task_far_deadline, reference_time
    )
