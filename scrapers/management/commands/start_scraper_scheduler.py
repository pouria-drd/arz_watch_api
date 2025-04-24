import os
import signal
import logging
from dotenv import load_dotenv
from django.core.management import call_command
from django.core.management.base import BaseCommand
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.blocking import BlockingScheduler

# Load environment variables
load_dotenv()

# Logging setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Configs from .env
initial_run = os.getenv("INITIAL_RUN", "False") == "True"
interval_trigger_minutes = int(os.getenv("INTERVAL_TRIGGER_MINUTES", 10))


class Command(BaseCommand):
    help = "Start the APScheduler for scrapers"

    def handle(self, *args, **options):
        logger.info("Starting the scraper scheduler...")

        scheduler = BlockingScheduler()

        def shutdown(signum, frame):
            logger.info("Shutting down scheduler...")
            scheduler.shutdown()

        signal.signal(signal.SIGTERM, shutdown)
        signal.signal(signal.SIGINT, shutdown)

        scrapers = [
            {
                "command": "run_tgju_scraper",
                "kwargs": {
                    "coins": True,
                    "gold": True,
                    "currency": True,
                    "save": True,
                },
                "id": "tgju_scraper",
            },
            {
                "command": "run_arzdigital_scraper",
                "kwargs": {"crypto": True, "save": True},
                "id": "arzdigital_scraper",
            },
        ]

        for scraper in scrapers:
            if initial_run:
                try:
                    logger.info(f"Running initial: {scraper['command']}")
                    call_command(scraper["command"], **scraper["kwargs"])
                except Exception as e:
                    logger.error(f"Initial run error for {scraper['command']}: {e}")

            scheduler.add_job(
                lambda c=scraper["command"], k=scraper["kwargs"]: call_command(c, **k),
                trigger=IntervalTrigger(minutes=interval_trigger_minutes),
                id=scraper["id"],
                replace_existing=True,
            )

        scheduler.start()
