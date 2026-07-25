"""
Roadmap module for TakeUForward SDE Sheet.
"""
import json
from pathlib import Path
from typing import List, Dict, Optional
from planner.models import Topic


class Roadmap:
    """Manages the TakeUForward SDE Sheet roadmap."""
    
    def __init__(self, tuf_sheet_path: str = "data/tuf_sheet.json"):
        """Initialize the roadmap from JSON file."""
        sheet_path = Path(tuf_sheet_path)
        if not sheet_path.exists():
            raise FileNotFoundError(f"TakeUForward sheet not found: {tuf_sheet_path}")
        
        with open(sheet_path, "r") as f:
            data = json.load(f)
        
        self.topics: List[Dict] = data.get("topics", [])
        self.system_design_topics: List[str] = data.get("systemDesignTopics", [])
    
    def get_total_topics(self) -> int:
        """Get total number of topics."""
        return len(self.topics)
    
    def get_topic_by_index(self, index: int) -> Optional[Dict]:
        """Get topic by index."""
        if 0 <= index < len(self.topics):
            return self.topics[index]
        return None
    
    def get_topic_by_name(self, name: str) -> Optional[Dict]:
        """Get topic by name."""
        for topic in self.topics:
            if topic.get("topic").lower() == name.lower():
                return topic
        return None
    
    def get_topic_index(self, topic_name: str) -> Optional[int]:
        """Get the index of a topic."""
        for idx, topic in enumerate(self.topics):
            if topic.get("topic").lower() == topic_name.lower():
                return idx
        return None
    
    def get_next_topic(self, current_topic: str) -> Optional[Dict]:
        """Get the next topic after the current one."""
        current_idx = self.get_topic_index(current_topic)
        if current_idx is not None and current_idx < len(self.topics) - 1:
            return self.topics[current_idx + 1]
        return None
    
    def get_remaining_topics(self, current_topic: str) -> List[Dict]:
        """Get all remaining topics after the current one."""
        current_idx = self.get_topic_index(current_topic)
        if current_idx is not None:
            return self.topics[current_idx + 1:]
        return []
    
    def get_completed_topics(self, current_topic: str) -> List[Dict]:
        """Get all completed topics up to (not including) the current one."""
        current_idx = self.get_topic_index(current_topic)
        if current_idx is not None:
            return self.topics[:current_idx]
        return []
    
    def get_system_design_topic_by_index(self, index: int) -> Optional[str]:
        """Get system design topic by index."""
        if 0 <= index < len(self.system_design_topics):
            return self.system_design_topics[index]
        return None
    
    def get_total_system_design_topics(self) -> int:
        """Get total number of system design topics."""
        return len(self.system_design_topics)
