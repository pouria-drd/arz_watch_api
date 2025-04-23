from .coinex_script import run_scraper
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Scrape CoinEx data and save it to file"

    def add_arguments(self, parser):
        parser.add_argument(
            "--crypto",
            action="store_true",
            help="Scrape crypto data only",
        )

        parser.add_argument(
            "--save",
            action="store_true",
            help="Save data to file",
        )

    def handle(self, *args, **kwargs):
        crypto = kwargs["crypto"]
        save = kwargs["save"]

        # Run the scraper with the provided arguments
        run_scraper(
            crypto=crypto,
            save=save,
        )
