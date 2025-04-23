from typing import Any
from bs4 import BeautifulSoup, Tag
from .base import CoinExBaseScraper
from datetime import datetime, timezone
from scrapers.modules.logger import LoggerFactory


class CoinExCryptoScraper(CoinExBaseScraper):
    ALLOWED_COINS = {
        "Litecoin",
        "Toncoin",
        "Tron",
        "Cardano",
        "Dogecoin",
        "Solana",
        "Ripple",
        "Ethereum",
        "Bitcoin",
    }

    COIN_FA_NAMES = {
        "Bitcoin": "بیت‌کوین",
        "Ethereum": "اتریوم",
        "Ripple": "ریپل",
        "Solana": "سولانا",
        "Dogecoin": "دوج‌کوین",
        "Cardano": "کاردانو",
        "Tron": "ترون",
        "Toncoin": "تون‌کوین",
        "Litecoin": "لایت‌کوین",
    }

    def __init__(self):
        super().__init__(
            url="https://www.coinex.com/en/markets/coin",
            scraper_type="Crypto",
            logger=LoggerFactory.get_logger(
                "CoinExCryptoScraper", "scrapers/coinex/crypto"
            ),
        )

    def _extract_rows(self, html: str) -> list[Tag]:
        soup = BeautifulSoup(html, "html.parser")
        return soup.select("tr.body-row")

    def _process_rows(self, rows: list[Tag]) -> list[dict[str, Any]]:
        result = []
        for row in rows:
            try:
                columns = row.find_all("td")
                name_tag = columns[2].select_one("span.text-16")
                full_name_tag = columns[2].select_one("span.coin-full-name span")
                price_tag = columns[3].select_one("span")
                change_tag = columns[4].select_one("span")
                market_cap_tag = columns[5].select_one("span")
                vol_24h_tag = columns[6].select_one("span")

                coin_name = full_name_tag.text.strip() if full_name_tag else None
                if coin_name not in self.ALLOWED_COINS:
                    continue

                result.append(
                    {
                        "symbol": name_tag.text.strip() if name_tag else None,
                        "name": coin_name,
                        "name_fa": self.COIN_FA_NAMES.get(coin_name),
                        "price_usd": (
                            price_tag.text.strip().replace(",", "")
                            if price_tag
                            else None
                        ),
                        "change_24h": change_tag.text.strip() if change_tag else None,
                        "market_cap": (
                            market_cap_tag.text.strip() if market_cap_tag else None
                        ),
                        "volume_24h": vol_24h_tag.text.strip() if vol_24h_tag else None,
                        "last_update": datetime.now(timezone.utc).isoformat(),
                    }
                )
            except Exception as e:
                self.logger.warning(f"Failed to parse row: {e}")
        return result
