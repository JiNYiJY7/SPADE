from __future__ import annotations
from datetime import datetime, timedelta
from typing import Dict, List
from ..models import Task, TimeSlot, StudySession, Plan


def plan_sessions(
    tasks_sorted: List[Task],
    free_slots: List[TimeSlot],
    now: datetime,
    chunk_minutes: int = 50,
    break_minutes: int = 10,
    min_session_minutes: int = 15,
) -> Plan:
    """
    Simple scheduler:
    - Fill free time slots from now onward
    - Allocate sessions by priority order
    - Split large tasks into chunks
    - Insert short breaks
    """
    sessions: List[StudySession] = []
    remaining: Dict[str, int] = {t.id: t.remaining_minutes for t in tasks_sorted}

    for slot in free_slots:
        cursor = max(slot.start, now)
        slot_end = slot.end

        while cursor < slot_end:
            # pick first task with remaining time
            pick = None
            for t in tasks_sorted:
                if remaining[t.id] > 0:
                    pick = t
                    break
            if pick is None:
                break

            available_minutes = int((slot_end - cursor).total_seconds() // 60)
            if available_minutes < min_session_minutes:
                break

            study_minutes = min(chunk_minutes, remaining[pick.id], available_minutes)
            if study_minutes < min_session_minutes:
                break

            start = cursor
            end = cursor + timedelta(minutes=study_minutes)

            sessions.append(
                StudySession(
                    task_id=pick.id,
                    title=pick.title,
                    start=start,
                    end=end,
                    minutes=study_minutes,
                )
            )

            remaining[pick.id] -= study_minutes
            cursor = end + timedelta(minutes=break_minutes)

    return Plan(generated_at=now, sessions=sessions)
