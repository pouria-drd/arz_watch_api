import time
import json
import platform
from selenium import webdriver
from django.conf import settings
from typing import Any, Generator
from bs4 import BeautifulSoup, Tag
from abc import ABC, abstractmethod
from contextlib import contextmanager
from datetime import datetime, timezone
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


class TGJUBaseScraper(ABC):
    """Abstract base class for scraping TGJU price tables."""

    _platform = platform.system()

    def __init__(self, url: str, logger, scraper_type: str, timeout: int = 10):
        self.url = url
        self.driver = None
        self.logger = logger
        self.timeout = timeout
        self.scraper_type = scraper_type

    def fetch_data(self, pretty: bool = False) -> list[dict[str, Any]] | None:
        self.logger.info(f"Fetching {self.scraper_type} data from TGJU...")

        try:
            with self._get_driver() as driver:
                self.driver = driver
                page_content = self._load_page()
                rows = self._extract_rows(page_content)
                data = self._process_rows(rows)

                self.logger.info(f"{self.scraper_type} data successfully scraped.")
                return (
                    json.dumps(data, ensure_ascii=False, indent=4) if pretty else data
                )

        except TimeoutException:
            self.logger.warning("Page load timed out.")
        except WebDriverException as e:
            self.logger.critical(f"WebDriver failed: {str(e)}")
        except Exception as e:
            self.logger.exception(f"Unexpected error: {str(e)}")
        return None

    @contextmanager
    def _get_driver(
        self, auto_driver: bool = False
    ) -> Generator[webdriver.Chrome, None, None]:
        """Get a new Chrome driver instance."""
        # Initialize the driver path based on the platform
        linux_path = (
            settings.BASE_DIR / "scrapers/drivers/chrome_driver_linux/chromedriver"
        )
        windows_path = (
            settings.BASE_DIR
            / "scrapers/drivers/chrome_driver_windows/chromedriver.exe"
        )

        driver_path = windows_path if self._platform == "Windows" else linux_path

        # Initialize the service based on the auto_driver flag
        service = (
            Service(driver_path)
            if not auto_driver
            else Service(ChromeDriverManager().install())
        )

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
        driver = webdriver.Chrome(service=service, options=options)

        try:
            yield driver
        finally:
            driver.quit()

    def _load_page(self) -> str:
        self.driver.get(self.url)
        WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tr[data-market-row]"))
        )
        time.sleep(5)  # wait for the page to fully load (you can adjust this)
        return self.driver.page_source

    def _extract_rows(self, content: str) -> list[Tag]:
        soup = BeautifulSoup(content, "html.parser")
        return soup.find_all("tr", {"data-market-row": True})

    def _process_rows(self, rows: list[Tag]) -> list[dict[str, str]]:
        seen = set()
        result = []

        for row in rows:
            if not self._is_relevant_row(row):
                continue

            title = self._format_title(row.find("th").text.strip())
            if title in seen:
                continue
            seen.add(title)
            result.append(self._parse_row(row, title))

        return result

    def _format_title(self, title: str) -> str:
        return title.replace(" / 750", "") if "750" in title else title

    def _clean_price(self, price: str) -> str:
        return price.strip().replace(",", "")

    def _extract_change(self, change_data: Tag) -> tuple[str, str]:
        change_text = change_data.text.strip()
        if ")" in change_text:
            parts = change_text.split(")")
            change_percentage = parts[0] + ")"
            change_amount = parts[1].strip().replace(",", "")
        else:
            change_percentage, change_amount = "0%", "0"
        return change_percentage, change_amount

    def _is_negative_change(self, change_data: Tag) -> bool:
        return change_data.find("span", class_="low")

    def _parse_row(self, row: Tag, title: str) -> dict[str, str]:
        columns = row.find_all("td")
        price = self._clean_price(columns[0].text)
        change_data = columns[1]
        change_percentage, change_amount = self._extract_change(change_data)
        is_negative = self._is_negative_change(change_data)

        return {
            "title": title,
            "price": price,
            "change_percentage": f"{'-' if is_negative else ''}{change_percentage[1:-2]}%",
            "change_amount": f"{'-' if is_negative else ''}{change_amount}",
            "last_update": datetime.now(timezone.utc).isoformat(),
        }

    @abstractmethod
    def _is_relevant_row(self, row: Tag) -> bool:
        """Determine if a row should be processed."""
        pass
