from .config import DB_CONFIG, HEADERS
from .database import DatabaseExecution
from .gsmarena_crawler import MainScraper, RateLimitError

def main():
    """
    Scrape phone data and save to database.
    Returns True if any data was successfully saved, False if completely empty.
    """
    db_repo = None
    all_phones_data = []

    try:
        db_repo = DatabaseExecution(DB_CONFIG)
        db_repo.create_table()

        scraper = MainScraper(HEADERS)
        samsung_url = "https://www.gsmarena.com/samsung-phones-f-9-0-r1-p1.php"
        
        all_phones_data = scraper.get_phones_spec(samsung_url, limit=20)

        if all_phones_data:
            scraped_count = len(all_phones_data)
            print(f"Data fetched: {scraped_count} phones. Saving to database...")
            db_repo.insert_data(all_phones_data)
            return True
        else:
            print("No data was scraped")
            return False

    except RateLimitError as e:
        print(f"Rate limit detected.")
        if all_phones_data and db_repo:
            scraped_count = len(all_phones_data)
            print(f"Saving {scraped_count} fetched records before exit...")
            try:
                db_repo.insert_data(all_phones_data)
                print(f"Successfully saved {scraped_count} records")
                return True
            except Exception as db_error:
                print(f"Error saving data: {db_error}")
                return False
        else:
            print("No data fetched before rate limit")
            return False

    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
        return False

    finally:
        if db_repo:
            db_repo.close()

if __name__ == "__main__":
    main()