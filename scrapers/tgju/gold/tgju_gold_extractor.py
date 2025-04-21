from scrapers.logger import LoggerFactory
from scrapers.tgju.base import TGJUBaseScraper


class TGJUGoldScraper(TGJUBaseScraper):
    def __init__(self):
        super().__init__(
            url="https://www.tgju.org/gold-chart",
            scraper_type="Gold",
            logger=LoggerFactory.get_logger("TGJUGoldScraper", "scrapers/tgju/gold"),
        )

    def _is_relevant_row(self, row) -> bool:
        titles = ["طلای 18 عیار / 750", "مثقال طلا"]
        title = row.find("th").text.strip()
        return title in titles
