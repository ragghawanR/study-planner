"""
Scheduling module for determining daily workload.
"""
from enum import Enum
from datetime import datetime, timedelta
from typing import Optional


class DayOfWeek(Enum):
    """Day of the week enum."""
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class ContestType(Enum):
    """Type of contest."""
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"


class WorkloadProfile(Enum):
    """Daily workload profile."""
    LIGHT = "light"          # 1-2 hours
    MEDIUM = "medium"        # 2-3 hours
    HEAVY = "heavy"          # 4-5 hours
    CONTEST = "contest"      # Contest day
    REVISION_ONLY = "revision"  # Revision only


class SchedulingRules:
    """Manages scheduling logic for daily study plans."""
    
    def __init__(self):
        """Initialize scheduling rules."""
        self.weekday = None
        self.is_contest_day = False
        self.contest_type: Optional[ContestType] = None
    
    def set_date(self, date: datetime = None) -> None:
        """Set the date for scheduling."""
        if date is None:
            date = datetime.now()
        self.weekday = DayOfWeek(date.weekday())
    
    def set_contest_day(self, contest_type: ContestType) -> None:
        """Mark as contest day."""
        self.is_contest_day = True
        self.contest_type = contest_type
    
    def clear_contest_day(self) -> None:
        """Clear contest day flag."""
        self.is_contest_day = False
        self.contest_type = None
    
    def get_workload_profile(self, date: datetime = None) -> WorkloadProfile:
        """
        Determine the workload profile for a given date.
        
        Rules:
        - Weekdays (Mon-Fri): Medium - focus on concepts
        - Saturday with biweekly contest: Contest
        - Saturday otherwise: Heavy - problem solving
        - Sunday with weekly contest: Contest
        - Sunday otherwise: Heavy - problem solving
        """
        if date is None:
            date = datetime.now()
        
        self.set_date(date)
        
        if self.is_contest_day:
            return WorkloadProfile.CONTEST
        
        if self.weekday in [DayOfWeek.MONDAY, DayOfWeek.TUESDAY, 
                            DayOfWeek.WEDNESDAY, DayOfWeek.THURSDAY, DayOfWeek.FRIDAY]:
            return WorkloadProfile.MEDIUM
        
        if self.weekday == DayOfWeek.SATURDAY:
            return WorkloadProfile.HEAVY
        
        if self.weekday == DayOfWeek.SUNDAY:
            return WorkloadProfile.HEAVY
    
    def get_daily_schedule(self, date: datetime = None) -> dict:
        """Get the daily schedule for a given date."""
        if date is None:
            date = datetime.now()
        
        self.set_date(date)
        workload = self.get_workload_profile(date)
        day_name = self.weekday.name.capitalize()
        
        schedule = {
            "date": date.isoformat(),
            "day": day_name,
            "workload_profile": workload.value,
            "is_contest_day": self.is_contest_day,
            "contest_type": self.contest_type.value if self.contest_type else None,
        }
        
        # Add workload-specific instructions
        if workload == WorkloadProfile.MEDIUM:
            schedule.update({
                "focus": "Concepts and Problem Solving",
                "estimated_time_hours": 3,
                "problems_to_solve": "3-5",
                "system_design": True,
                "revision": True,
                "notes": "Focus on concept understanding. Solve 3-5 problems. Review one system design topic."
            })
        
        elif workload == WorkloadProfile.HEAVY:
            schedule.update({
                "focus": "Problem Solving",
                "estimated_time_hours": 4,
                "problems_to_solve": "5-7",
                "system_design": False,
                "revision": True,
                "notes": "Focus on solving more problems. Light revision."
            })
        
        elif workload == WorkloadProfile.CONTEST:
            if self.contest_type == ContestType.WEEKLY:
                schedule.update({
                    "focus": "Weekly Contest + Upsolve",
                    "estimated_time_hours": 3,
                    "problems_to_solve": "Contest + Upsolve",
                    "system_design": False,
                    "revision": True,
                    "notes": "Participate in weekly contest. Upsolve after. Revision only after."
                })
            elif self.contest_type == ContestType.BIWEEKLY:
                schedule.update({
                    "focus": "Biweekly Contest + Upsolve",
                    "estimated_time_hours": 3,
                    "problems_to_solve": "Contest + Upsolve + max 2",
                    "system_design": False,
                    "revision": False,
                    "notes": "Participate in biweekly contest. Upsolve. Maximum 2 additional problems."
                })
        
        elif workload == WorkloadProfile.REVISION_ONLY:
            schedule.update({
                "focus": "Revision Only",
                "estimated_time_hours": 2,
                "problems_to_solve": "0",
                "system_design": False,
                "revision": True,
                "notes": "Focus on revising previously solved problems."
            })
        
        return schedule
    
    def get_this_weeks_schedule(self, start_date: datetime = None) -> list:
        """Get the schedule for the entire week."""
        if start_date is None:
            start_date = datetime.now()
        
        # Find Monday of the week
        monday = start_date - timedelta(days=start_date.weekday())
        
        week_schedule = []
        for i in range(7):  # 7 days in a week
            day = monday + timedelta(days=i)
            week_schedule.append(self.get_daily_schedule(day))
        
        return week_schedule
    
    @staticmethod
    def is_leetcode_contest_week(date: datetime = None) -> dict:
        """
        Determine if there's a contest this week.
        
        Note: LeetCode Weekly Contest happens every Sunday.
        LeetCode Biweekly Contest happens every other Saturday.
        
        This is a placeholder - in production, fetch from LeetCode API.
        """
        if date is None:
            date = datetime.now()
        
        # Weekly contests are always on Sunday
        days_until_sunday = (6 - date.weekday()) % 7
        if days_until_sunday == 0:
            return {"has_contest": True, "type": "weekly", "day": "Sunday"}
        
        # Biweekly contests are on alternating Saturdays
        # This is a simplified check - real implementation should verify with LeetCode
        days_until_saturday = (5 - date.weekday()) % 7
        if days_until_saturday == 0:
            return {"has_contest": True, "type": "biweekly", "day": "Saturday"}
        
        return {"has_contest": False, "type": None, "day": None}
