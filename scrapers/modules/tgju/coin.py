from bs4 import Tag
from .base import TGJUBaseScraper
from scrapers.modules.logger import LoggerFactory


class TGJUCoinScraper(TGJUBaseScraper):
    RELEVANT_TITLES = {
        "ربع سکه",
        "نیم سکه",
        "سکه امامی",
        "سکه بهار آزادی",
    }

    def __init__(self):
        super().__init__(
            url="https://www.tgju.org/coin",
            scraper_type="Coin",
            logger=LoggerFactory.get_logger("TGJUCoinScraper", "scrapers/tgju/coin"),
        )

    def _is_relevant_row(self, row: Tag) -> bool:
        title = row.find("th").text.strip()
        return title in self.RELEVANT_TITLES
