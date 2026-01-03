from __future__ import annotations
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class Task(BaseModel):
    id: str
    title: str
    due: datetime
    estimated_minutes: int
    remaining_minutes: int
    importance: int = Field(ge=1, le=5, default=3)
    subject: Optional[str] = None


class TimeSlot(BaseModel):
    start: datetime
    end: datetime

    @property
    def minutes(self) -> int:
        return int((self.end - self.start).total_seconds() // 60)


class StudySession(BaseModel):
    task_id: str
    title: str
    start: datetime
    end: datetime
    minutes: int


class Plan(BaseModel):
    generated_at: datetime
    sessions: List[StudySession] = []
