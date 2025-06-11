# Prospects_DB FastAPI Service

This service provides a FastAPI-based REST API to fetch lead data from a PostgreSQL database.

## Features

- Connects to a PostgreSQL database using SQLAlchemy.
- Loads configuration from a `.env` file.
- Exposes an endpoint to retrieve all leads with status "new" from the `hackathon.lead` table.
- Returns results as a list of structured JSON objects.

## Requirements

Install dependencies with:

```sh
pip install -r requirements.txt
```

## Usage

1. Ensure your `.env` file is configured with the correct database credentials.
2. Start the FastAPI server:

```sh
uvicorn main:app --reload
```

3. Access the API at [http://localhost:8000/leads/](http://localhost:8000/leads/)

## API Endpoint

- `GET /leads/`  
  Returns a list of leads with status "new" from the database.

## Code Overview

- Loads environment variables using `python-dotenv`.
- Connects to PostgreSQL using SQLAlchemy.
- Defines a Pydantic model `Lead` for response validation.
- Uses dependency injection for database sessions.
- Handles errors with appropriate HTTP status codes.

See [main.py](Browser-use-implementation/Prospects_DB/main.py) for implementation details.