"""
Main orchestration script for the study planner.
Runs the complete pipeline: load context -> generate prompt -> call LLM -> send via Telegram.
"""
import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv

# Setup logging
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

log_file = logs_dir / f"planner_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

from planner.roadmap import Roadmap
from planner.progress import ProgressTracker
from planner.scheduler import SchedulingRules
from planner.prompt_builder import PromptBuilder
from planner.llm import LLMClient
from telegram.telegram_bot import TelegramBot


def validate_environment() -> bool:
    """Validate that all required environment variables are set."""
    logger.info("=" * 60)
    logger.info("🎓 AI SDE Coach - Daily Study Plan Generation")
    logger.info("=" * 60)
    
    required_vars = {
        "OPENAI_API_KEY": "OpenAI API Key",
        "TELEGRAM_BOT_TOKEN": "Telegram Bot Token",
        "TELEGRAM_CHAT_ID": "Telegram Chat ID"
    }
    
    missing_vars = []
    for var, desc in required_vars.items():
        if not os.getenv(var):
            missing_vars.append(desc)
            logger.warning(f"✗ {desc} not found")
        else:
            logger.info(f"✓ {desc} found")
    
    if missing_vars:
        logger.error(f"\n❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    logger.info("\n✅ All environment variables validated")
    return True


def main():
    """Main orchestration function."""
    try:
        # Validate environment
        if not validate_environment():
            logger.error("❌ Environment validation failed. Exiting.")
            return False
        
        # Initialize components
        logger.info("\n📚 Initializing components...")
        
        try:
            roadmap = Roadmap("data/tuf_sheet.json")
            logger.info(f"✓ Roadmap loaded ({roadmap.get_total_topics()} topics)")
        except Exception as e:
            logger.error(f"✗ Failed to load roadmap: {e}")
            return False
        
        try:
            progress_tracker = ProgressTracker("data/progress.json")
            logger.info(f"✓ Progress tracker initialized")
        except Exception as e:
            logger.error(f"✗ Failed to initialize progress tracker: {e}")
            return False
        
        try:
            scheduler = SchedulingRules()
            logger.info(f"✓ Scheduler initialized")
        except Exception as e:
            logger.error(f"✗ Failed to initialize scheduler: {e}")
            return False
        
        # Get today's context
        logger.info("\n📋 Building today's context...")
        today_schedule = scheduler.get_daily_schedule(datetime.now())
        logger.info(f"✓ Today: {today_schedule['day']} - {today_schedule['workload_profile']} workload")
        logger.info(f"  Focus: {today_schedule['focus']}")
        logger.info(f"  Estimated time: {today_schedule['estimated_time_hours']} hours")
        
        # Build prompt
        logger.info("\n🤖 Building prompt for LLM...")
        try:
            prompt_builder = PromptBuilder(roadmap, progress_tracker, scheduler)
            context = prompt_builder.get_prompt_context(datetime.now())
            logger.info(f"✓ Context built:")
            logger.info(f"  Current topic: {context['current_topic']}")
            logger.info(f"  Next topic: {context['next_topic']}")
            
            prompt = prompt_builder.build_daily_prompt(datetime.now())
        except Exception as e:
            logger.error(f"✗ Failed to build prompt: {e}")
            return False
        
        # Generate study plan using LLM
        logger.info("\n🔄 Calling OpenAI API...")
        try:
            llm_client = LLMClient()
            study_plan = llm_client.generate_study_plan(prompt)
            
            if not study_plan:
                logger.error("✗ Failed to generate study plan")
                return False
            
            logger.info("✓ Study plan generated successfully")
            logger.info(f"  Summary: {study_plan.summary[:100]}...")
            logger.info(f"  Tasks: {len(study_plan.tasks)} tasks")
            logger.info(f"  Revision items: {len(study_plan.revision)} items")
        except Exception as e:
            logger.error(f"✗ Error during LLM generation: {e}")
            return False
        
        # Send via Telegram
        logger.info("\n📨 Sending study plan via Telegram...")
        try:
            telegram_bot = TelegramBot()
            
            if not telegram_bot.validate_credentials():
                logger.error("✗ Failed to validate Telegram credentials")
                return False
            
            logger.info("✓ Telegram bot authenticated")
            
            if telegram_bot.send_study_plan(study_plan, today_schedule['day']):
                logger.info("✓ Study plan sent successfully")
            else:
                logger.error("✗ Failed to send study plan via Telegram")
                return False
        
        except Exception as e:
            logger.error(f"✗ Error sending Telegram message: {e}")
            return False
        
        # Update progress
        logger.info("\n💾 Updating progress...")
        try:
            progress_tracker.update_last_study_date()
            logger.info("✓ Progress updated")
        except Exception as e:
            logger.error(f"✗ Failed to update progress: {e}")
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ Daily study plan generation completed successfully!")
        logger.info("=" * 60)
        return True
    
    except Exception as e:
        logger.error(f"\n❌ Unexpected error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
