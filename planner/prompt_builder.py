"""
Prompt builder for generating study plan prompts.
"""
from datetime import datetime
from typing import Dict, List
from planner.roadmap import Roadmap
from planner.progress import ProgressTracker
from planner.scheduler import SchedulingRules


class PromptBuilder:
    """Builds structured prompts for the LLM."""
    
    def __init__(self, roadmap: Roadmap, progress: ProgressTracker, scheduler: SchedulingRules):
        """Initialize the prompt builder."""
        self.roadmap = roadmap
        self.progress = progress
        self.scheduler = scheduler
    
    def build_daily_prompt(self, date: datetime = None) -> str:
        """
        Build a structured prompt for daily study plan generation.
        
        Returns a deterministic prompt containing all context needed for the LLM.
        """
        if date is None:
            date = datetime.now()
        
        # Get all context
        schedule = self.scheduler.get_daily_schedule(date)
        current_topic = self.progress.get_current_topic()
        next_topic_obj = self.roadmap.get_next_topic(current_topic)
        next_topic = next_topic_obj.get("topic") if next_topic_obj else "N/A"
        completed_topics = self.progress.get_completed_topics()
        completed_problems = self.progress.get_completed_problems()
        revision_queue = self.progress.get_revision_queue()
        current_sd = self.progress.get_current_system_design_topic()
        
        prompt = f"""You are an AI Study Coach helping a student prepare for software engineering interviews using the TakeUForward roadmap.

## Today's Context
- **Date**: {date.strftime('%A, %B %d, %Y')}
- **Day**: {schedule['day']}
- **Workload Profile**: {schedule['workload_profile'].upper()}
- **Focus**: {schedule['focus']}
- **Estimated Study Time**: {schedule['estimated_time_hours']} hours

## Study Progress
- **Current Topic**: {current_topic}
- **Next Topic**: {next_topic}
- **Completed Topics**: {len(completed_topics)} topics
- **Total Problems Solved**: {self.progress.get_total_problems_solved()} problems
- **Revision Queue Size**: {len(revision_queue)} problems

## Scheduling Rules for Today
- **Problems to Solve**: {schedule['problems_to_solve']}
- **System Design**: {"Yes" if schedule['system_design'] else "No"}
- **Include Revision**: {"Yes" if schedule['revision'] else "No"}
- **Notes**: {schedule['notes']}

## Today's System Design Topic
- **Current Focus**: {current_sd}

## Revision Queue (problems to review)
{self._format_revision_queue(revision_queue)}

## Task
Generate a personalized daily study plan for today that:
1. Is specific and actionable
2. Respects the workload profile and time constraints
3. Follows the scheduling rules
4. Maintains focus on the current topic
5. Includes time estimates for each task
6. Provides motivational context

Return the plan in this JSON format:
{{
    "summary": "Brief overview of today's study plan (1-2 sentences)",
    "tasks": [
        "Task 1: Description",
        "Task 2: Description",
        ...
    ],
    "revision": [
        "Revision task 1",
        "Revision task 2",
        ...
    ],
    "motivation": "A motivational message for the day",
    "estimated_time_hours": {schedule['estimated_time_hours']}
}}

Ensure the response is valid JSON."""
        
        return prompt
    
    def _format_revision_queue(self, revision_queue: List[str]) -> str:
        """Format revision queue for display."""
        if not revision_queue:
            return "No problems in revision queue."
        
        formatted = "Problems to review:\n"
        for i, problem in enumerate(revision_queue[:10], 1):  # Show first 10
            formatted += f"{i}. {problem}\n"
        
        if len(revision_queue) > 10:
            formatted += f"... and {len(revision_queue) - 10} more\n"
        
        return formatted
    
    def get_prompt_context(self, date: datetime = None) -> Dict:
        """
        Get the context dictionary used to build the prompt.
        
        Useful for debugging and understanding what context was used.
        """
        if date is None:
            date = datetime.now()
        
        schedule = self.scheduler.get_daily_schedule(date)
        current_topic = self.progress.get_current_topic()
        next_topic_obj = self.roadmap.get_next_topic(current_topic)
        next_topic = next_topic_obj.get("topic") if next_topic_obj else "N/A"
        
        return {
            "date": date.isoformat(),
            "day": schedule['day'],
            "workload_profile": schedule['workload_profile'],
            "current_topic": current_topic,
            "next_topic": next_topic,
            "completed_topics_count": len(self.progress.get_completed_topics()),
            "total_problems_solved": self.progress.get_total_problems_solved(),
            "revision_queue_size": len(self.progress.get_revision_queue()),
            "current_system_design": self.progress.get_current_system_design_topic(),
            "estimated_time_hours": schedule['estimated_time_hours'],
            "focus": schedule['focus'],
            "notes": schedule['notes']
        }
