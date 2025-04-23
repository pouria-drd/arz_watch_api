from scrapers.modules.coinex import CoinExScraperManager


def run_scraper(crypto=True, save=True):
    scraper_manager = CoinExScraperManager()

    scraper_manager.run(
        crypto=crypto,
        save=save,
    )
