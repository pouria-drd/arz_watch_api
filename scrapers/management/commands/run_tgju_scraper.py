from .tgju_script import run_scraper
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Scrape TGJU data and save it to file"

    def add_arguments(self, parser):
        parser.add_argument(
            "--coins",
            action="store_true",
            help="Scrape coin data only",
        )

        parser.add_argument(
            "--gold",
            action="store_true",
            help="Scrape gold data only",
        )

        parser.add_argument(
            "--currency",
            action="store_true",
            help="Scrape currency data only",
        )

        parser.add_argument(
            "--save",
            action="store_true",
            help="Saves data to file",
        )

    def handle(self, *args, **kwargs):
        coins = kwargs["coins"]
        gold = kwargs["gold"]
        currency = kwargs["currency"]
        save = kwargs["save"]

        # Run the scraper with the provided arguments
        run_scraper(
            coins=coins,
            gold=gold,
            currency=currency,
            save=save,
        )
        self.stdout.write(self.style.SUCCESS("Successfully ran the TGJU scraper"))
