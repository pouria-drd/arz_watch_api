import os
import json
from django.conf import settings
from .crypto import ArzDigitalCryptoScraper

SCRAPERS_OUTPUT_DIR = settings.BASE_DIR / "scrapers_output" / "arzdigital"


class ArzDigitalScraperManager:
    def __init__(self):
        self.crypto_scraper = ArzDigitalCryptoScraper()

    def _save_to_file(self, data, filename: str):
        """Internal method to save data to a JSON file."""
        if data:
            path = SCRAPERS_OUTPUT_DIR / filename
            os.makedirs(path.parent, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

    def get_crypto_data(self, save: bool = True):
        data = self.crypto_scraper.fetch_data()
        if save:
            self._save_to_file(data, "crypto.json")
        else:
            return data

    def run(self, crypto=False, save=True):
        """Run the selected scrapers. If no specific flag is given, scrape all."""
        results = {}

        if not crypto:
            results["crypto"] = self.get_crypto_data(save=save)
        else:
            if crypto:
                results["crypto"] = self.get_crypto_data(save=save)

        return results
