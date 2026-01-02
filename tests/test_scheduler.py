from datetime import datetime
from study_planner.models import Task, TimeSlot
from study_planner.utils.scheduler import plan_sessions


def test_scheduler_sessions_within_slot():
    now = datetime.fromisoformat("2026-01-02T10:00:00")
    tasks = [
        Task(id="A", title="Task A", due=datetime.fromisoformat("2026-01-03T10:00:00"),
             est_minutes=120, remaining_minutes=120, importance=5)
    ]
    slots = [
        TimeSlot(
            start=datetime.fromisoformat("2026-01-02T10:00:00"),
            end=datetime.fromisoformat("2026-01-02T12:00:00"),
        )
    ]

    plan = plan_sessions(tasks_sorted=tasks, free_slots=slots, now=now, chunk_minutes=50, break_minutes=10)
    for s in plan.sessions:
        assert slots[0].start <= s.start <= slots[0].end
        assert slots[0].start <= s.end <= slots[0].end
        assert s.end > s.start
