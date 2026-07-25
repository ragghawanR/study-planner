"""
Progress tracking module.
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List
from planner.models import Progress


class ProgressTracker:
    """Manages user progress in study plan."""
    
    def __init__(self, progress_file: str = "data/progress.json"):
        """Initialize progress tracker."""
        self.progress_file = Path(progress_file)
        self._ensure_file_exists()
        self.progress = self._load_progress()
    
    def _ensure_file_exists(self) -> None:
        """Ensure progress file exists."""
        if not self.progress_file.exists():
            self.progress_file.parent.mkdir(parents=True, exist_ok=True)
            default_progress = {
                "current_topic": "Arrays",
                "completed_topics": [],
                "completed_problems": [],
                "revision_queue": [],
                "current_system_design": "Caching",
                "last_study_date": None,
                "total_problems_solved": 0
            }
            with open(self.progress_file, "w") as f:
                json.dump(default_progress, f, indent=2)
    
    def _load_progress(self) -> dict:
        """Load progress from file."""
        with open(self.progress_file, "r") as f:
            return json.load(f)
    
    def _save_progress(self) -> None:
        """Save progress to file."""
        with open(self.progress_file, "w") as f:
            json.dump(self.progress, f, indent=2)
    
    def get_current_topic(self) -> str:
        """Get current topic."""
        return self.progress.get("current_topic", "Arrays")
    
    def set_current_topic(self, topic: str) -> None:
        """Set current topic."""
        self.progress["current_topic"] = topic
        self._save_progress()
    
    def get_completed_topics(self) -> List[str]:
        """Get list of completed topics."""
        return self.progress.get("completed_topics", [])
    
    def complete_topic(self, topic: str) -> None:
        """Mark a topic as completed."""
        if topic not in self.progress["completed_topics"]:
            self.progress["completed_topics"].append(topic)
            self._save_progress()
    
    def get_completed_problems(self) -> List[str]:
        """Get list of completed problems."""
        return self.progress.get("completed_problems", [])
    
    def complete_problem(self, problem: str) -> None:
        """Mark a problem as completed."""
        if problem not in self.progress["completed_problems"]:
            self.progress["completed_problems"].append(problem)
            self.progress["total_problems_solved"] = len(self.progress["completed_problems"])
            self._save_progress()
    
    def get_revision_queue(self) -> List[str]:
        """Get revision queue."""
        return self.progress.get("revision_queue", [])
    
    def add_to_revision_queue(self, problem: str) -> None:
        """Add problem to revision queue."""
        if problem not in self.progress["revision_queue"]:
            self.progress["revision_queue"].append(problem)
            self._save_progress()
    
    def remove_from_revision_queue(self, problem: str) -> None:
        """Remove problem from revision queue."""
        if problem in self.progress["revision_queue"]:
            self.progress["revision_queue"].remove(problem)
            self._save_progress()
    
    def get_current_system_design_topic(self) -> str:
        """Get current system design topic."""
        return self.progress.get("current_system_design", "Caching")
    
    def set_current_system_design_topic(self, topic: str) -> None:
        """Set current system design topic."""
        self.progress["current_system_design"] = topic
        self._save_progress()
    
    def get_last_study_date(self) -> Optional[str]:
        """Get last study date."""
        return self.progress.get("last_study_date")
    
    def update_last_study_date(self) -> None:
        """Update last study date to today."""
        self.progress["last_study_date"] = datetime.now().isoformat()
        self._save_progress()
    
    def get_total_problems_solved(self) -> int:
        """Get total problems solved."""
        return self.progress.get("total_problems_solved", 0)
    
    def reset_progress(self) -> None:
        """Reset all progress."""
        self.progress = {
            "current_topic": "Arrays",
            "completed_topics": [],
            "completed_problems": [],
            "revision_queue": [],
            "current_system_design": "Caching",
            "last_study_date": None,
            "total_problems_solved": 0
        }
        self._save_progress()
    
    def get_progress_summary(self) -> dict:
        """Get a summary of progress."""
        return {
            "current_topic": self.get_current_topic(),
            "completed_topics": len(self.get_completed_topics()),
            "completed_problems": len(self.get_completed_problems()),
            "revision_queue_size": len(self.get_revision_queue()),
            "current_system_design": self.get_current_system_design_topic(),
            "last_study_date": self.get_last_study_date(),
            "total_problems_solved": self.get_total_problems_solved()
        }
