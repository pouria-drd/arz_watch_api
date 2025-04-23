from bs4 import Tag
from .base import TGJUBaseScraper
from scrapers.modules.logger import LoggerFactory


class TGJUGoldScraper(TGJUBaseScraper):
    RELEVANT_TITLES = {
        "مثقال طلا",
        "طلای 18 عیار / 750",
        "طلای ۲۴ عیار",
        "آبشده نقدی",
        "حباب آبشده",
    }

    def __init__(self):
        super().__init__(
            url="https://www.tgju.org/gold-chart",
            scraper_type="Gold",
            logger=LoggerFactory.get_logger("TGJUGoldScraper", "scrapers/tgju/gold"),
        )

    def _is_relevant_row(self, row: Tag) -> bool:
        title = row.find("th").text.strip()
        return title in self.RELEVANT_TITLES
