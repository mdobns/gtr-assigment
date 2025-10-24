from .config import DB_CONFIG,HEADERS
from .database import DatabaseExecution
from .gsmarena_crawler import MainScraper

def main():
    db_repo = None

    try:
        db_repo = DatabaseExecution(DB_CONFIG)
        db_repo.create_table()

        scraper = MainScraper(HEADERS)
        samsung_url = "https://www.gsmarena.com/samsung-phones-f-9-0-r1-p1.php"

        all_phones_data = scraper.get_phones_spec(samsung_url, limit=25)  # Increased to 25 models to ensure we get enough data

        if all_phones_data:
            db_repo.insert_data(all_phones_data)
        else:
            print("No data were scraped")

    except Exception as e:
        # Print the actual exception instance and type for easier debugging
        print(f"Unhandled exception: {type(e).__name__}: {e}")

    finally:
        if db_repo:
            db_repo.close()

if __name__ == "__main__":
    main()