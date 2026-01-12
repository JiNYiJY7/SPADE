from __future__ import annotations
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class Task(BaseModel):
    """
    Represents a single academic task or assignment.

    This model exists to:
    - Store all relevant task information consistently
    - Enable validation (e.g., importance must be 1-5)
    - Support scheduling, reminders, and progress tracking
    """

    id: str  # Unique identifier for the task
    title: str  # Human-readable title of the task
    due: datetime  # Task deadline used for prioritization
    estimated_minutes: int  # Total expected effort in minutes
    remaining_minutes: int  # Work left to complete the task
    importance: int = Field(ge=1, le=5, default=3)  
    # Importance scale 1-5 ensures consistent prioritization
    subject: Optional[str] = None  # Optional categorization of task


class TimeSlot(BaseModel):
    """
    Represents a period of available time where tasks can be scheduled.

    This model exists to:
    - Define availability for the scheduling engine
    - Enable calculation of duration for planning
    """

    start: datetime  # Start time of the available slot
    end: datetime  # End time of the available slot

    @property
    def minutes(self) -> int:
        """
        Return the duration of the time slot in whole minutes.

        This property exists to:
        - Provide a consistent unit of measurement for scheduling
        - Avoid repeated inline duration calculations in planner logic
        """
        return int((self.end - self.start).total_seconds() // 60)


class StudySession(BaseModel):
    """
    Represents a scheduled session for a task within a plan.

    This model exists to:
    - Link a task to a specific time period in the plan
    - Provide structured information for display or reminders
    """

    task_id: str  # ID of the task assigned to this session
    title: str  # Task title (redundant for convenience in display)
    start: datetime  # Scheduled start time of the session
    end: datetime  # Scheduled end time of the session
    minutes: int  # Duration of the session in minutes


class Plan(BaseModel):
    """
    Represents a complete execution plan containing multiple study sessions.

    This model exists to:
    - Store the output of the scheduling engine
    - Allow inspection, logging, and reminders generation
    - Capture the time when the plan was generated
    """

    generated_at: datetime  # Timestamp for when the plan was created
    sessions: List[StudySession] = []  # Ordered list of scheduled study sessions
