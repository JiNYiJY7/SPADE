from datetime import datetime
from study_planner.models import Task
from study_planner.utils.scoring import priority_score


def test_priority_deadline_closer_higher():
    now = datetime.fromisoformat("2026-01-02T10:00:00")
    t1 = Task(id="1", title="Close", due=datetime.fromisoformat("2026-01-02T12:00:00"),
              est_minutes=60, remaining_minutes=60, importance=3)
    t2 = Task(id="2", title="Far", due=datetime.fromisoformat("2026-01-05T12:00:00"),
              est_minutes=60, remaining_minutes=60, importance=3)

    assert priority_score(t1, now) > priority_score(t2, now)
