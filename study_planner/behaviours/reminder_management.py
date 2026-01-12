from __future__ import annotations
from datetime import datetime
from typing import List
from ..models import Task


def determine_reminder_priority(hours_until_due: float) -> str:
    """
    Determine the reminder priority level based on how close a task is to its deadline.

    The goal of this function is to control notification frequency:
    - Urgent tasks require frequent reminders to prevent missed deadlines.
    - Distant deadlines should not overwhelm the user with notifications.

    Args:
        hours_until_due (float): Number of hours remaining before the task deadline.

    Returns:
        str: Human-readable reminder priority and frequency description.
    """

    # Very urgent: task is due soon, frequent reminders are necessary
    if hours_until_due <= 6:
        return "HIGH (every 30–60 min)"

    # Moderately urgent: task is due within a day
    if hours_until_due <= 24:
        return "MEDIUM (every 2–3 hours)"

    # Low urgency: task is still a few days away
    if hours_until_due <= 72:
        return "LOW (daily)"

    # Informational: deadline is far away, minimal reminders needed
    return "INFO (every few days)"


def generate_task_reminders(
    sorted_tasks: List[Task], current_time: datetime
) -> List[str]:
    """
    Generate reminder messages for active tasks based on urgency and remaining work.

    This function exists to:
    - Filter out completed tasks (no reminders needed)
    - Calculate time-to-deadline dynamically
    - Assign an appropriate reminder urgency level
    - Produce human-readable reminder messages for UI or chatbot display

    Args:
        sorted_tasks (List[Task]): Tasks already sorted by priority.
        current_time (datetime): Current system time for deadline comparison.

    Returns:
        List[str]: A list of formatted reminder messages.
    """

    reminder_messages: List[str] = []

    for task in sorted_tasks:
        # Skip completed tasks to avoid unnecessary or confusing reminders
        if task.remaining_minutes <= 0:
            continue

        # Calculate how many hours remain before the task deadline
        # This enables dynamic urgency calculation rather than fixed schedules
        hours_until_due = (
            task.due - current_time
        ).total_seconds() / 3600.0

        # Determine how aggressively the user should be reminded
        priority_label = determine_reminder_priority(hours_until_due)

        # Build a user-friendly reminder message
        reminder_messages.append(
            f"[{priority_label}] "
            f"{task.title} | "
            f"due in {hours_until_due:.1f}h | "
            f"remaining {task.remaining_minutes} min"
        )

    return reminder_messages
