from scrapers.logger import LoggerFactory
from scrapers.tgju.base import TGJUBaseScraper


class TGJUCoinScraper(TGJUBaseScraper):
    def __init__(self):
        super().__init__(
            url="https://www.tgju.org/coin",
            scraper_type="Coin",
            logger=LoggerFactory.get_logger("TGJUCoinScraper", "scrapers/tgju/coin"),
        )

    def _is_relevant_row(self, row) -> bool:
        titles = ["ربع سکه", "نیم سکه", "سکه امامی", "سکه بهار آزادی"]
        title = row.find("th").text.strip()
        return title in titles
