# Task 2: Scraper + RAG API

## Overview

This task is a FastAPI-based web service that combines web scraping with Retrieval-Augmented Generation (RAG). It scrapes phone specifications from GSMarena, stores them in a database, and provides an AI-powered query interface using Google's Generative AI.

## Features

- **Web Scraping**: Crawls GSMarena for phone specifications and data
- **RAG (Retrieval-Augmented Generation)**: Answers questions about phones using AI
- **RESTful API**: FastAPI endpoints for querying phone data
- **CORS Support**: Enables cross-origin requests for frontend integration

## Prerequisites

Make sure you have completed the main project setup:

1. ✅ Created virtual environment (`venv`)
2. ✅ Activated the virtual environment
3. ✅ Installed dependencies from `requirements.txt`
4. ✅ PostgreSQL installed and running
5. ✅ Google Generative AI API key set up

If not, go back to the main [README.md](../README.md) and follow the setup instructions.

## How to Run

From the **main project directory** (`pythonProjectAssignment`), run:

```powershell
uvicorn Task2.main:app --reload
```

### What This Does

1. Starts the FastAPI server on `http://localhost:8000`
   2. It will check for the database , if the table does not exist or table is empty it first get the data from `Gsmarena.com` and then start the server.
2. Enables hot-reloading (`--reload` flag) for development

### Access Points

- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc (ReDoc)
- **Root Endpoint**: http://localhost:8000 (returns welcome message)

## API Endpoints

### GET `/`
Returns a welcome message.

**Response:**
```json
{
  "message": "Welcome to the Scraper + RAG API"
}
```

### GET/POST `/ask`
Query phone data using natural language with RAG.

**Query Parameter:**
- `question` (string): Your question about phones

**Example:**
```
http://localhost:8000/ask?question=What%20are%20the%20best%20budget%20phones%3F
```

**Response:**
```json
{
  "question": "What are the best budget phones?",
  "answer": "Based on available data, phones under $300 include..."
}
```

## Project Structure

```
Task2/
├── main.py                           # FastAPI app entry point
├── api/
│   └── ask_routes.py                # API route handlers
├── datascraper/
│   ├── __init__.py
│   ├── config.py                    # Database configuration
│   ├── database.py                  # Database operations
│   ├── gsmarena_crawler.py          # Web scraper
│   └── main.py                      # Scraper execution
├── rag/
│   ├── __init__.py
│   ├── generative_rag.py            # RAG implementation
│   ├── rag.py                       # RAG utilities
└── __pycache__/
```

## Configuration

### Database Setup (config.py)

Edit `Task2/datascraper/config.py` to configure your PostgreSQL connection according to your setup:

```python
DB_CONFIG = {
    "host": "localhost",           # PostgreSQL server address
    "port": 5432,                  # PostgreSQL port (default: 5432)
    "database": "phone_database",  # Database name
    "user": "postgres",            # PostgreSQL username
    "password": "your_password"    # PostgreSQL password
}
```

**Configuration steps:**
1. Open `Task2/datascraper/config.py`
2. Replace the values with your PostgreSQL credentials:
   - `host`: Where your PostgreSQL server is running (e.g., `localhost`, `127.0.0.1`, or a remote IP)
   - `port`: PostgreSQL port (default is `5432`)
   - `database`: Name of your database
   - `user`: Your PostgreSQL username
   - `password`: Your PostgreSQL password

### Google Generative AI Setup

1. Get an API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Set environment variable:
   ```powershell
   $env:GOOGLE_API_KEY = "your_api_key_here"
   ```
   Or add to your configuration file

## Development

### With Hot-Reload (Recommended)
```powershell
uvicorn Task2.main:app --reload
```

### Production Mode (No Hot-Reload)
```powershell
uvicorn Task2.main:app
```

### Custom Port
```powershell
uvicorn Task2.main:app --reload --port 8001
```

## How It Works

### RAG Pipeline

1. **Question Input**: User asks a question about phones
2. **Retrieval**: Query available phone data
3. **Augmentation**: Combine retrieved data with the question
4. **Generation**: Use Google Generative AI to create answer
5. **Response**: Return AI-generated answer to user

## Dependencies Used

- `fastapi` - Modern web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `psycopg2` - PostgreSQL adapter
- `beautifulsoup4` - Web scraping
- `requests` - HTTP requests
- `google-generativeai` - Google AI API

## Troubleshooting

### "ModuleNotFoundError: No module named 'Task2'"
- Ensure you're running from the **main project directory**
- Verify the virtual environment is activated

### "Address already in use" Error
- Port 8000 is occupied. Use a different port:
  ```powershell
  uvicorn Task2.main:app --reload --port 8001
  ```

### Database Connection Error
- Verify PostgreSQL is running
- Check your database credentials in `Task2/datascraper/config.py`
- Ensure database exists and user has proper permissions
- Test connection with: `psql -h localhost -U postgres -d phone_database`

### "Google API Key not found"
- Set the environment variable before running:
  ```powershell
  $env:GOOGLE_API_KEY = "your_key"
  ```

## Testing the API

### Using Swagger UI (Easiest)
1. Go to http://localhost:8000/docs
2. Click on `/ask` endpoint
3. Type your question
4. Click "Try it out"

### Using PowerShell
```powershell
$response = Invoke-WebRequest -Uri "http://localhost:8000/ask?question=What%20phones%20have%205G?" -Method Get
$response.Content | ConvertFrom-Json
```

### Using curl
```bash
curl "http://localhost:8000/ask?question=Best%20gaming%20phones"
```

## Performance Notes

- First request may be slower due to database queries
- Scraper runs automatically on first startup
- Subsequent requests are faster with caching
- Use `--reload` only during development

## Security Considerations

- Current CORS allows all origins (`"*"`)
- In production, restrict to specific domains
- Implement rate limiting for the API
- Secure database credentials in `config.py` (never commit with real credentials)

## Related Documentation

- [Main README](../README.md) - Project overview and setup
- [Task 1 README](../Task1/README.md) - Alternative task documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Google Generative AI Docs](https://ai.google.dev/docs)
