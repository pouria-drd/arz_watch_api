from scrapers.logger import LoggerFactory
from scrapers.tgju.base import TGJUBaseScraper


class TGJUCurrencyScraper(TGJUBaseScraper):
    def __init__(self):
        super().__init__(
            url="https://www.tgju.org/currency",
            scraper_type="Currency",
            logger=LoggerFactory.get_logger(
                "TGJUCurrencyScraper", "scrapers/tgju/currency"
            ),
        )

    def _is_relevant_row(self, row) -> bool:
        titles = [
            "دلار",
            "یورو",
            "یوان چین",
            "درهم امارات",
            "پوند انگلیس",
            "لیر ترکیه",
            "روبل روسیه",
        ]
        title = row.find("th").text.strip()
        return title in titles
