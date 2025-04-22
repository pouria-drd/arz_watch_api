from django.apps import AppConfig
from django.core.management import call_command
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler

can_run = False


class ScrapersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "scrapers"

    def ready(self):
        if can_run:
            # First, run the task immediately
            call_command(
                "run_tgju_scraper",
                coins=True,
                gold=True,
                currency=True,
                no_save=False,
            )

            # Then set up the scheduler to run it every 5 minutes
            scheduler = BackgroundScheduler()

            # Schedule the management command to run every 5 minutes
            scheduler.add_job(
                lambda: call_command(
                    "run_tgju_scraper",
                    coins=True,
                    gold=True,
                    currency=True,
                    no_save=False,
                ),
                IntervalTrigger(minutes=5),
                id="tgju_scraper_scheduler",
                replace_existing=True,
            )

            scheduler.start()
