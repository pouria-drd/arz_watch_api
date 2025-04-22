import os
import json
from django.conf import settings
from .coin import TGJUCoinScraper
from .gold import TGJUGoldScraper
from .currency import TGJUCurrencyScraper

SCRAPERS_OUTPUT_DIR = settings.BASE_DIR / "scrapers_output" / "tgju"


class TGJUScraperManager:
    def __init__(self):
        self.coin_scraper = TGJUCoinScraper()
        self.gold_scraper = TGJUGoldScraper()
        self.currency_scraper = TGJUCurrencyScraper()

    def _save_to_file(self, data, filename: str):
        """Internal method to save data to a JSON file."""
        if data:
            path = SCRAPERS_OUTPUT_DIR / filename
            os.makedirs(path.parent, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

    def get_coin_data(self, save: bool = False):
        data = self.coin_scraper.fetch_data()
        if save:
            self._save_to_file(data, "coin.json")
        else:
            return data

    def get_gold_data(self, save: bool = False):
        data = self.gold_scraper.fetch_data()
        if save:
            self._save_to_file(data, "gold.json")
        else:
            return data

    def get_currency_data(self, save: bool = False):
        data = self.currency_scraper.fetch_data()
        if save:
            self._save_to_file(data, "currency.json")
        else:
            return data

    def run(self, coins=False, gold=False, crypto=False, currency=False, save=True):
        """Run the selected scrapers. If no specific flag is given, scrape all."""
        results = {}
        # If no specific flags are provided, scrape all
        if not (coins or gold or currency):
            results["coins"] = self.get_coin_data(save=save)
            results["gold"] = self.get_gold_data(save=save)
            results["currency"] = self.get_currency_data(save=save)
        else:
            if coins:
                results["coins"] = self.get_coin_data(save=save)

            if gold:
                results["gold"] = self.get_gold_data(save=save)

            if currency:
                results["currency"] = self.get_currency_data(save=save)

        return results
