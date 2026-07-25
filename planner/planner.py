"""
Main entry point for the study planner.
"""
import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from planner.roadmap import Roadmap
from planner.progress import ProgressTracker
from planner.scheduler import SchedulingRules
from planner.prompt_builder import PromptBuilder
from planner.llm import LLMClient
from telegram.telegram_bot import TelegramBot
from planner.models import StudyPlan

# Load environment variables
load_dotenv()


def main():
    """Main function."""
    print("🎓 AI SDE Coach - Study Planner")
    print("=" * 50)
    
    # Check environment variables
    openai_key = os.getenv("OPENAI_API_KEY")
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    print("\n✅ Environment Check:")
    print(f"  OpenAI API Key: {'✓' if openai_key else '✗ Missing'}")
    print(f"  Telegram Bot Token: {'✓' if telegram_token else '✗ Missing'}")
    print(f"  Telegram Chat ID: {'✓' if telegram_chat_id else '✗ Missing'}")
    
    # Test roadmap loading
    try:
        roadmap = Roadmap("data/tuf_sheet.json")
        print("\n✅ Roadmap Loaded:")
        print(f"  Total Topics: {roadmap.get_total_topics()}")
    except Exception as e:
        print(f"\n❌ Error loading roadmap: {e}")
        return
    
    # Test progress tracking
    try:
        progress_tracker = ProgressTracker("data/progress.json")
        print("\n✅ Progress Tracker Initialized:")
        summary = progress_tracker.get_progress_summary()
        print(f"  Current Topic: {summary['current_topic']}")
    except Exception as e:
        print(f"\n❌ Error loading progress: {e}")
        return
    
    # Test scheduling rules
    try:
        scheduler = SchedulingRules()
        today_schedule = scheduler.get_daily_schedule(datetime.now())
        print("\n✅ Scheduler Initialized:")
        print(f"  Today ({today_schedule['day']}): {today_schedule['workload_profile']} workload")
    except Exception as e:
        print(f"\n❌ Error with scheduler: {e}")
        return
    
    # Test prompt builder
    try:
        prompt_builder = PromptBuilder(roadmap, progress_tracker, scheduler)
        context = prompt_builder.get_prompt_context(datetime.now())
        print("\n✅ Prompt Builder Initialized:")
        print(f"  Current Topic: {context['current_topic']}")
    except Exception as e:
        print(f"\n❌ Error with prompt builder: {e}")
        return
    
    # Test LLM client
    print("\n✅ LLM Client:")
    if openai_key:
        try:
            llm_client = LLMClient()
            print("  OpenAI client initialized")
        except Exception as e:
            print(f"  ✗ Error initializing LLM client: {e}")
    else:
        print("  ⚠️  Skipped (OpenAI API key not configured)")
    
    # Test Telegram bot
    print("\n✅ Telegram Bot:")
    if telegram_token and telegram_chat_id:
        try:
            telegram_bot = TelegramBot()
            print("  Telegram bot initialized")
            
            if telegram_bot.validate_credentials():
                print("  ✓ Bot credentials validated")
                
                # Create a sample study plan for testing
                sample_plan = StudyPlan(
                    summary="Study arrays and solve practice problems",
                    tasks=["Learn array basics", "Solve 3 problems", "Review time complexity"],
                    revision=["Two Sum", "Best Time to Buy and Sell Stock"],
                    motivation="You're building a strong foundation. Keep going!",
                    estimated_time_hours=3
                )
                
                print("\n  📨 Sending sample study plan...")
                if telegram_bot.send_study_plan(sample_plan, "Sunday"):
                    print("  ✓ Sample study plan sent successfully!")
            else:
                print("  ✗ Failed to validate bot credentials")
        except Exception as e:
            print(f"  ✗ Error with Telegram bot: {e}")
    else:
        print("  ⚠️  Skipped (Telegram credentials not configured)")
    
    print("\n✅ Milestones 1-7 Complete!")
    print("   Next step:")
    print("   - Milestone 8: GitHub Actions Setup")


if __name__ == "__main__":
    main()
