import time
import json
import platform
from selenium import webdriver
from django.conf import settings
from typing import Any, Generator
from bs4 import BeautifulSoup, Tag
from abc import ABC, abstractmethod
from contextlib import contextmanager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


class ArzDigitalBaseScraper(ABC):
    """Abstract base class for scraping crypto data from ArzDigital website."""

    _platform = platform.system()

    def __init__(self, url: str, logger, scraper_type: str, timeout: int = 10):
        self.url = url
        self.driver = None
        self.logger = logger
        self.timeout = timeout
        self.scraper_type = scraper_type

    def fetch_data(self, pretty: bool = False) -> list[dict[str, Any]] | None:
        self.logger.info(f"Fetching {self.scraper_type} data from ArzDigital...")

        try:
            with self._get_driver() as driver:
                self.driver = driver
                page_content = self._load_page()
                rows = self._extract_rows(page_content)
                data = self._process_rows(rows)

                self.logger.info(
                    f"{self.scraper_type} data successfully scraped from ArzDigital."
                )
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
            EC.presence_of_element_located((By.CSS_SELECTOR, "tr.arz-coin-tr"))
        )
        time.sleep(5)  # wait for the page to fully load (you can adjust this)
        return self.driver.page_source

    def _extract_rows(self, content: str) -> list[Tag]:
        soup = BeautifulSoup(content, "html.parser")
        return soup.find_all("tr", class_="arz-coin-tr")

    @abstractmethod
    def _process_rows(self, rows: list[Tag]) -> list[dict[str, str]]:
        """Process rows to extract relevant data."""
        pass
