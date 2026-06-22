import argparse
import sys
import uvicorn
from src.scraper import run_scraper
from src.parser import run_parser
from src.db import init_db, insert_records

def main():
    parser = argparse.ArgumentParser(description="DGCA Aviation Stats Pipeline")
    parser.add_argument("--scrape", action="store_true", help="Run the scraper to download files")
    parser.add_argument("--parse", action="store_true", help="Run the parser to extract data and ingest into DB")
    parser.add_argument("--serve", action="store_true", help="Run the FastAPI backend server")
    parser.add_argument("--years", nargs="+", default=["2025"], help="List of years to scrape/parse")
    
    args = parser.parse_args()
    
    if not (args.scrape or args.parse or args.serve):
        parser.print_help()
        sys.exit(1)
        
    if args.scrape:
        print(f"Scraping reports for years: {args.years}")
        run_scraper(limit_years=args.years)
        
    if args.parse:
        print("Initializing database...")
        init_db()
        print("Parsing and ingesting reports...")
        records = run_parser()
        if records:
            insert_records(records)
        else:
            print("No records found to ingest.")
            
    if args.serve:
        print("Starting FastAPI backend server...")
        # Note: we use reload=True only if running from terminal directly, but uvicorn.run accepts a string when reload=True.
        # To avoid reload issues on Windows in packaged directories, we can set reload=False.
        uvicorn.run("src.api:app", host="127.0.0.1", port=8000, reload=False)

if __name__ == "__main__":
    main()
