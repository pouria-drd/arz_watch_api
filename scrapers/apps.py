import os
from dotenv import load_dotenv
from django.apps import AppConfig
from django.core.management import call_command
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv()

initial_run = os.getenv("INITIAL_RUN", "False") == "True"
interval_trigger_minutes = int(os.getenv("INTERVAL_TRIGGER_MINUTES", 10))


class ScrapersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "scrapers"
    _scheduler = None  # Class-level reference to the scheduler

    def ready(self):
        """Initialize the schedulers when the app is ready."""
        if not self._should_run_schedulers():
            return

        self._initialize_scheduler()
        self._setup_scrapers(initial_run=initial_run)

    def _should_run_schedulers(self):
        """Determine if schedulers should run (helps prevent duplicate runs in some Django setups)."""
        # You could add more sophisticated checks here if needed
        return True

    def _initialize_scheduler(self):
        """Initialize a single shared scheduler instance."""
        if self._scheduler is None:
            self._scheduler = BackgroundScheduler()
            self._scheduler.start()

    def _setup_scrapers(self, initial_run=False):
        """Configure all scraper schedules."""
        scrapers = [
            {
                "command": "run_tgju_scraper",
                "kwargs": {
                    "coins": True,
                    "gold": True,
                    "currency": True,
                    "save": True,
                },
                "id": "tgju_scraper_scheduler",
            },
            # {
            #     "command": "run_coinex_scraper",
            #     "kwargs": {"crypto": True, "save": True},
            #     "id": "coinex_scraper_scheduler",
            # },
        ]

        for scraper in scrapers:
            self._schedule_scraper(
                command=scraper["command"],
                kwargs=scraper["kwargs"],
                job_id=scraper["id"],
                initial_run=initial_run,
            )

    def _schedule_scraper(self, command, kwargs, job_id, initial_run=False):
        """Schedule a single scraper command."""
        if initial_run:
            call_command(command, **kwargs)

        if self._scheduler is not None:
            self._scheduler.add_job(
                lambda: call_command(command, **kwargs),
                IntervalTrigger(minutes=interval_trigger_minutes),
                id=job_id,
                replace_existing=True,
            )
