from selenium import webdriver
from typing import Generator, Any
from abc import ABC, abstractmethod
from contextlib import contextmanager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC


class CoinExBaseScraper(ABC):
    def __init__(self, url: str, logger, scraper_type: str, timeout: int = 10):
        self.url = url
        self.logger = logger
        self.timeout = timeout
        self.driver = None
        self.scraper_type = scraper_type

    @contextmanager
    def _get_driver(self) -> Generator[webdriver.Chrome, None, None]:
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        try:
            yield driver
        finally:
            driver.quit()

    def _load_page(self) -> str:
        self.driver.get(self.url)
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "tr.body-row"))
            )
            return self.driver.page_source
        except TimeoutException:
            self.logger.error("Timeout while waiting for CoinEx page to load.")
            return ""

    @abstractmethod
    def _extract_rows(self, html: str) -> list[Any]:
        pass

    @abstractmethod
    def _process_rows(self, rows: list[Any]) -> list[dict[str, Any]]:
        pass

    def fetch_data(self) -> list[dict[str, Any]] | None:
        self.logger.info(f"Fetching {self.scraper_type} data from CoinEx...")
        try:
            with self._get_driver() as driver:
                self.driver = driver
                page_content = self._load_page()
                if not page_content:
                    return None
                rows = self._extract_rows(page_content)
                self.logger.info(f"{self.scraper_type} data successfully scraped.")
                return self._process_rows(rows)
        except Exception as e:
            self.logger.error(f"Error during scraping: {e}")
            return None
