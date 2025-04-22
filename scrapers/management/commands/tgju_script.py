from scrapers.modules.tgju import TGJUScraperManager


def run_scraper(coins=False, gold=False, crypto=False, currency=False, save=True):
    scraper_manager = TGJUScraperManager()

    scraper_manager.run(
        coins=coins,
        gold=gold,
        currency=currency,
        save=save,
    )
