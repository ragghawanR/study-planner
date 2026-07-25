"""
Telegram Bot module for sending study plans.
"""
import os
from typing import Optional
import requests

from planner.models import StudyPlan


class TelegramBot:
    """Manages Telegram bot communication."""
    
    def __init__(self, bot_token: Optional[str] = None, chat_id: Optional[str] = None):
        """Initialize Telegram bot."""
        self.bot_token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")
        
        if not self.bot_token or not self.chat_id:
            raise ValueError(
                "TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be provided "
                "or set in environment variables"
            )
        
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    def send_study_plan(self, study_plan: StudyPlan, day_name: str = "Today") -> bool:
        """
        Send formatted study plan to Telegram.
        
        Args:
            study_plan: The StudyPlan object to send
            day_name: The day of the week (e.g., "Monday")
            
        Returns:
            True if successful, False otherwise
        """
        try:
            message = self._format_study_plan(study_plan, day_name)
            return self.send_message(message)
        except Exception as e:
            print(f"❌ Error sending study plan: {e}")
            return False
    
    def send_message(self, text: str) -> bool:
        """
        Send a text message to Telegram.
        
        Args:
            text: The message text
            
        Returns:
            True if successful, False otherwise
        """
        try:
            payload = {
                "chat_id": self.chat_id,
                "text": text,
                "parse_mode": "Markdown"
            }
            
            response = requests.post(
                f"{self.api_url}/sendMessage",
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✓ Telegram message sent successfully")
                return True
            else:
                print(f"✗ Telegram API error: {response.status_code}")
                print(f"  Response: {response.text}")
                return False
        
        except requests.exceptions.Timeout:
            print("✗ Telegram API request timed out")
            return False
        except requests.exceptions.ConnectionError:
            print("✗ Failed to connect to Telegram API")
            return False
        except Exception as e:
            print(f"✗ Error sending Telegram message: {e}")
            return False
    
    def _format_study_plan(self, study_plan: StudyPlan, day_name: str) -> str:
        """
        Format study plan as Telegram message.
        
        Args:
            study_plan: The StudyPlan object
            day_name: The day of the week
            
        Returns:
            Formatted message string
        """
        message = f"""📅 {day_name}

*Today's Focus*
{'─' * 30}
{study_plan.summary}

*Tasks*
{'─' * 30}
"""
        
        # Add tasks
        for i, task in enumerate(study_plan.tasks, 1):
            message += f"{i}. {task}\n"
        
        # Add revision
        if study_plan.revision:
            message += f"\n*Revision*\n{'─' * 30}\n"
            for i, item in enumerate(study_plan.revision, 1):
                message += f"{i}. {item}\n"
        
        # Add motivation
        message += f"\n*💪 Motivation*\n{'─' * 30}\n{study_plan.motivation}\n"
        
        # Add time estimate
        message += f"\n⏱️  Estimated Time: {study_plan.estimated_time_hours} hours\n"
        message += "\nGood luck! 🚀"
        
        return message
    
    def validate_credentials(self) -> bool:
        """
        Validate bot token and chat ID by making a test request.
        
        Returns:
            True if credentials are valid, False otherwise
        """
        try:
            # Try to get bot info
            response = requests.get(
                f"{self.api_url}/getMe",
                timeout=5
            )
            
            if response.status_code == 200:
                bot_info = response.json()
                if bot_info.get("ok"):
                    print(f"✓ Bot authenticated as: @{bot_info['result'].get('username')}")
                    return True
            
            print(f"✗ Failed to authenticate bot: {response.text}")
            return False
        
        except Exception as e:
            print(f"✗ Error validating bot credentials: {e}")
            return False
    
    def send_test_message(self) -> bool:
        """Send a test message to verify bot works."""
        test_message = """🤖 *AI SDE Coach - Test Message*

This is a test message to verify Telegram integration.

✓ If you see this, the bot is working correctly!"""
        
        return self.send_message(test_message)
