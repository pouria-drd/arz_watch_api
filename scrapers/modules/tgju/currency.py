from bs4 import Tag
from .base import TGJUBaseScraper
from scrapers.modules.logger import LoggerFactory


class TGJUCurrencyScraper(TGJUBaseScraper):
    RELEVANT_TITLES = {
        "دلار",
        "یورو",
        "یوان چین",
        "درهم امارات",
        "پوند انگلیس",
        "لیر ترکیه",
        "روبل روسیه",
    }

    def __init__(self):
        super().__init__(
            url="https://www.tgju.org/currency",
            scraper_type="Currency",
            logger=LoggerFactory.get_logger(
                "TGJUCurrencyScraper", "scrapers/tgju/currency"
            ),
        )

    def _is_relevant_row(self, row: Tag) -> bool:
        title = row.find("th").text.strip()
        return title in self.RELEVANT_TITLES
