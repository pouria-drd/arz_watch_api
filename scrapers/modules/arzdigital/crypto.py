from bs4 import Tag
from datetime import datetime, timezone
from .base import ArzDigitalBaseScraper
from datetime import datetime, timezone
from scrapers.modules.logger import LoggerFactory


class ArzDigitalCryptoScraper(ArzDigitalBaseScraper):
    TARGET_NAMES = {
        "Bitcoin": "بیت‌کوین",
        "Ethereum": "اتریوم",
        "XRP": "ریپل",
        "Solana": "سولانا",
        "Dogecoin": "دوج‌کوین",
        "Cardano": "کاردانو",
        "TRON": "ترون",
        "Toncoin": "تون‌کوین",
        "Litecoin": "لایت‌کوین",
        "Tether USDt": "تتر",
    }

    def __init__(self):
        super().__init__(
            url="https://arzdigital.com/coins/",
            scraper_type="Crypto",
            logger=LoggerFactory.get_logger(
                "ArzDigitalCryptoScraper", "scrapers/arzdigital/crypto"
            ),
        )

    def _process_rows(self, rows: list[Tag]) -> list[dict[str, str]]:
        crypto_data = []
        last_update = datetime.now(timezone.utc).isoformat()

        for row in rows:
            try:
                name = row.select_one("td.arz-coin-table__name-td span").text.strip()

                if name not in self.TARGET_NAMES:
                    continue

                symbol = row["data-symbol"]

                price_usd = row.select_one(
                    "td.arz-coin-table__price-td span"
                ).text.strip()

                price_irr_str = row.select_one(
                    "td.arz-coin-table__rial-price-td span"
                ).text.strip()

                price_irr = self._parse_price_irt(price_irr_str)

                marketcap = row.select_one(
                    "td.arz-coin-table__marketcap-td span[dir='auto']"
                ).text.strip()

                daily_change_elem = row.select_one(
                    "td.arz-coin-table__daily-swing-td span"
                )

                daily_change_text = daily_change_elem.text.strip()
                if "arz-negative" in daily_change_elem.get("class", []):
                    if not daily_change_text.startswith("-"):
                        daily_change_text = f"-{daily_change_text}"

                # weekly_change = row.select_one(
                #     "td.arz-coin-table__weekly-swing-td span"
                # ).text.strip()

                coin = {
                    "name": name,
                    "name_fa": self.TARGET_NAMES[name],
                    "symbol": symbol,
                    "price_usd": price_usd,
                    "price_irr": price_irr,
                    "market_cap": marketcap,
                    "change_24h": daily_change_text,
                    "last_update": last_update,
                }

                crypto_data.append(coin)

            except Exception as e:
                continue
        return crypto_data

    def _parse_price_irt(self, price_str: str) -> str:
        persian_digits = "۰۱۲۳۴۵۶۷۸۹"
        english_digits = "0123456789"
        trans_table = str.maketrans("".join(persian_digits), "".join(english_digits))
        clean_str = (
            price_str.translate(trans_table).replace(",", "").replace("ت", "").strip()
        )
        return str(int(clean_str) * 10)
