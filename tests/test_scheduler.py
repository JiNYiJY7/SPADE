"""
Unit Test: Scheduler Session Allocation

Purpose:
- Verify that the scheduler allocates study sessions entirely within available free slots.
- Ensures that no session starts before or ends after the provided time slot.
- Validates that session durations are logical (end > start).
"""

from datetime import datetime
from study_planner.models import Task, TimeSlot
from study_planner.utils.scheduler import plan_sessions


def test_scheduler_sessions_within_slot():
    """
    Test that planned study sessions fit entirely within defined free time slots.

    Why:
    - Core validation of the scheduler to respect available time.
    - Prevents unrealistic scheduling that would overlap unavailable periods.
    """
    # Reference current time for scheduling calculations
    reference_time = datetime.fromisoformat("2026-01-02T10:00:00")

    # Single high-priority task
    task_needing_time = [
        Task(
            id="A",
            title="Task A",
            due=datetime.fromisoformat("2026-01-03T10:00:00"),
            estimated_minutes=120,
            remaining_minutes=120,
            importance=5
        )
    ]

    # Available time slot for study (2 hours)
    available_slot = [
        TimeSlot(
            start=datetime.fromisoformat("2026-01-02T10:00:00"),
            end=datetime.fromisoformat("2026-01-02T12:00:00"),
        )
    ]

    # Generate the study plan
    # chunk_minutes: max duration of one session
    # break_minutes: break time between sessions
    study_plan = plan_sessions(
        tasks_sorted=task_needing_time,
        free_slots=available_slot,
        now=reference_time,
        chunk_minutes=50,
        break_minutes=10
    )

    # Validate each session is fully contained within the time slot
    for session in study_plan.sessions:
        assert available_slot[0].start <= session.start <= available_slot[0].end, \
            "Session start is outside available slot"
        assert available_slot[0].start <= session.end <= available_slot[0].end, \
            "Session end is outside available slot"
        assert session.end > session.start, "Session end time must be after start time"
