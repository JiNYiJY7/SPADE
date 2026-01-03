from __future__ import annotations 
from datetime import datetime, timedelta
from typing import Dict, List
from ..models import Task, TimeSlot, StudySession, Plan


def plan_sessions(
    tasks_sorted: List[Task],
    free_slots: List[TimeSlot],
    current_time: datetime,
    chunk_minutes: int = 50,
    break_minutes: int = 10,
    min_session_minutes: int = 15,
) -> Plan:
    """
    Simple scheduler:
    - Fill free time slots from current_time onward
    - Allocate sessions by priority order
    - Split large tasks into chunks
    - Insert short breaks
    """
    sessions: List[StudySession] = []
    remaining_minutes: Dict[str, int] = {task.id: task.remaining_minutes for task in tasks_sorted}

    for slot in free_slots:
        slot_cursor = max(slot.start, current_time)
        slot_end_time = slot.end

        while slot_cursor < slot_end_time:
            # pick first task with remaining time
            current_task = None
            for task in tasks_sorted:
                if remaining_minutes[task.id] > 0:
                    current_task = task
                    break

            if current_task is None:
                break

            available_minutes = int((slot_end_time - slot_cursor).total_seconds() // 60)
            if available_minutes < min_session_minutes:
                break

            study_minutes = min(chunk_minutes, remaining_minutes[current_task.id], available_minutes)
            if study_minutes < min_session_minutes:
                break

            session_start = slot_cursor
            session_end = slot_cursor + timedelta(minutes=study_minutes)

            sessions.append(
                StudySession(
                    task_id=current_task.id,
                    title=current_task.title,
                    start=session_start,
                    end=session_end,
                    minutes=study_minutes,
                )
            )

            remaining_minutes[current_task.id] -= study_minutes
            slot_cursor = session_end + timedelta(minutes=break_minutes)

    return Plan(generated_at=current_time, sessions=sessions)
