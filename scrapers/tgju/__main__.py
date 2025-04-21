import argparse
from scrapers.tgju import TGJUScraperManager


def main():
    parser = argparse.ArgumentParser(description="Scrape and save TGJU data.")
    parser.add_argument("--coins", action="store_true", help="Scrape coin data only")
    parser.add_argument("--gold", action="store_true", help="Scrape gold data only")
    parser.add_argument(
        "--currency", action="store_true", help="Scrape currency data only"
    )
    parser.add_argument(
        "--no-save", action="store_true", help="Only return data without saving to file"
    )

    args = parser.parse_args()

    scraper_manager = TGJUScraperManager()

    scraper_manager.run(
        coins=args.coins, gold=args.gold, currency=args.currency, save=not args.no_save
    )


if __name__ == "__main__":
    main()
