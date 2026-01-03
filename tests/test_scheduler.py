from datetime import datetime
from study_planner.models import Task, TimeSlot
from study_planner.utils.scheduler import plan_sessions


def test_scheduler_sessions_within_slot():
    current_time = datetime.fromisoformat("2026-01-02T10:00:00")
    task_list = [
        Task(id="A", title="Task A", due=datetime.fromisoformat("2026-01-03T10:00:00"),
             est_minutes=120, remaining_minutes=120, importance=5)
    ]
    time_slots = [
        TimeSlot(
            start=datetime.fromisoformat("2026-01-02T10:00:00"),
            end=datetime.fromisoformat("2026-01-02T12:00:00"),
        )
    ]

    study_plan = plan_sessions(tasks_sorted=task_list, free_slots=time_slots, now=current_time, chunk_minutes=50, break_minutes=10)
    for session in study_plan.sessions:
        assert time_slots[0].start <= session.start <= time_slots[0].end
        assert time_slots[0].start <= session.end <= time_slots[0].end
        assert session.end > session.start
