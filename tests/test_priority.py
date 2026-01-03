from datetime import datetime
from study_planner.models import Task
from study_planner.utils.scoring import priority_score


def test_priority_deadline_closer_higher():
    current_time = datetime.fromisoformat("2026-01-02T10:00:00")
    task_close_deadline = Task(id="1", title="Close", due=datetime.fromisoformat("2026-01-02T12:00:00"),
              estimated_minutes=60, remaining_minutes=60, importance=3)
    task_far_deadline = Task(id="2", title="Far", due=datetime.fromisoformat("2026-01-05T12:00:00"),
              estimated_minutes=60, remaining_minutes=60, importance=3)

    assert priority_score(task_close_deadline, current_time) > priority_score(task_far_dealine, current_time)
