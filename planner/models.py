"""
Data models for the study planner.
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class Problem(BaseModel):
    """Represents a coding problem."""
    name: str
    difficulty: str  # Easy, Medium, Hard


class Topic(BaseModel):
    """Represents a study topic."""
    topic: str
    difficulty: str
    problems: List[Problem]


class Progress(BaseModel):
    """User progress tracking."""
    current_topic: str
    completed_topics: List[str] = []
    completed_problems: List[str] = []
    revision_queue: List[str] = []
    current_system_design: str
    last_study_date: Optional[datetime] = None


class StudyPlan(BaseModel):
    """Generated daily study plan."""
    summary: str
    tasks: List[str]
    revision: List[str]
    motivation: str
    estimated_time_hours: int
