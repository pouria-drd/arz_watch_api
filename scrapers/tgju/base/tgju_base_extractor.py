import json
import time
from abc import ABC, abstractmethod
from datetime import datetime, timezone

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC


class TGJUBaseScraper(ABC):
    """Base class for scraping price data from TGJU"""

    def __init__(
        self, url: str, logger, scraper_type: str, timeout: int = 10, sleep: int = 5
    ):
        self.url = url
        self.driver = None
        self.sleep = sleep
        self.logger = logger
        self.timeout = timeout
        self.scraper_type = scraper_type

    def fetch_data(self, pretty: bool = False) -> list[dict[str, str]] | None:
        self.logger.info(f"Fetching {self.scraper_type} data from the TGJU website...")

        try:
            if self.driver is None:
                self.driver = self._initialize_driver()

            page_content = self._fetch_page_content()
            soup = self._parse_html(page_content)
            rows = self._get_table_rows(soup)
            self._close_driver()

            seen_titles = set()
            result = []

            for row in rows:
                if not self._is_relevant_row(row):
                    continue

                title = row.find("th").text.strip()
                title = self._format_title(title)

                if title in seen_titles:
                    continue

                seen_titles.add(title)
                result.append(self._parse_row(row))

            self.logger.info(
                f"{self.scraper_type} Data fetched successfully from TGJU website."
            )
            return (
                json.dumps(result, ensure_ascii=False, indent=4) if pretty else result
            )

        except Exception as e:
            self.logger.error(
                f"Failed to fetch {self.scraper_type} data from TGJU website: {e}"
            )
            return None
        finally:
            self._close_driver()

    def _initialize_driver(self):
        service = Service(ChromeDriverManager().install())
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        return webdriver.Chrome(service=service, options=chrome_options)

    def _fetch_page_content(self):
        self.driver.get(self.url)
        WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, "market-table"))
        )
        time.sleep(self.sleep)
        return self.driver.page_source

    def _parse_html(self, content):
        return BeautifulSoup(content, "html.parser")

    def _get_table_rows(self, soup):
        return soup.find_all("tr", {"data-market-row": True})

    def _parse_row(self, row):
        title = row.find("th").text.strip()
        title = self._format_title(title)

        price = self._clean_price(row.find_all("td")[0].text)
        change_data = row.find_all("td")[1]
        change_percentage, change_amount = self._extract_change(change_data)
        is_negative = self._is_negative_change(change_data)

        return {
            "title": title,
            "price": price,
            "change_percentage": f"{'-' if is_negative else ''}{change_percentage[1:-2]}%",
            "change_amount": f"{'-' if is_negative else ''}{change_amount}",
            "last_update": datetime.now(timezone.utc).isoformat(),
        }

    def _format_title(self, title: str) -> str:
        return title.replace(" / 750", "") if "750" in title else title

    def _clean_price(self, price: str) -> str:
        return price.strip().replace(",", "")

    def _extract_change(self, change_data):
        change_text = change_data.text.strip()
        change_percentage = change_text.split(")")[0] + ")"
        change_amount = change_text.split(")")[1].strip().replace(",", "")
        return change_percentage, change_amount

    def _is_negative_change(self, change_data) -> bool:
        return "low" in change_data.get("class", [])

    def _close_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    @abstractmethod
    def _is_relevant_row(self, row) -> bool:
        """Must be implemented by child classes"""
        pass
