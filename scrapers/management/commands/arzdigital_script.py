from scrapers.modules.arzdigital import ArzDigitalScraperManager


def run_scraper(crypto=True, save=True):
    scraper_manager = ArzDigitalScraperManager()

    scraper_manager.run(
        crypto=crypto,
        save=save,
    )
