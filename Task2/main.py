from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
from Task2.api.ask_routes import ask_router
from .datascraper import DatabaseExecution, DB_CONFIG, main

app = FastAPI(title="Scraper + RAG API")
db = DatabaseExecution(DB_CONFIG)

@app.on_event("startup")
def startup_event():
    """Check table, run scraper if table missing. Stop server if no data."""
    if not db.table_exists() or db.is_table_empty():
        print("Phones table not found. Running scraper...")
        scraping_success = main()
        
        if not scraping_success:
            print("ERROR: Scraping failed or no data retrieved. Cannot start server.")
            sys.exit(1)
    else:
        print("Phones table exists. Skipping scraper.")

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to the Scraper + RAG API"}

# Register /ask route
app.include_router(ask_router, prefix="", tags=["Ask"])

