import os
from typing import List
from dotenv import load_dotenv

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime

# Load environment variables from the .env file
load_dotenv()

# --- Database Connection Setup ---
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_SCHEMA = os.getenv("DB_SCHEMA")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a session-making class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Pydantic Model for API Response ---
# This model defines the shape of the data you'll send back.
# It ensures your API response is validated and well-structured.
class Lead(BaseModel):
    lead_id: int
    lead_first_name: str
    lead_last_name: str
    lead_company_name: str
    lead_official_title: str
    lead_type: str
    lead_generation_timestamp: datetime
    lead_generation_source: str
    lead_status: str
    lead_contact_number: str

    class Config:
        from_attributes = True  # Used to be orm_mode=True in Pydantic v1


# --- Dependency Injection for Database Session ---
# This function creates and yields a database session for each request
# and ensures it's closed afterward.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- FastAPI Application ---
app = FastAPI(
    title="Leads API",
    description="An API to fetch lead data from the hackathon database.",
    version="1.0.0"
)


@app.get("/leads/", response_model=List[Lead])
def get_all_leads(db: Session = Depends(get_db)):
    """
    Retrieve all leads from the database.
    
    This endpoint queries the hackathon.lead table and returns a list of all entries.
    """
    try:
        # Construct the SQL query using the schema from your .env file
        # Using text() from SQLAlchemy helps prevent SQL injection vulnerabilities
        query = text(f"""
            SELECT 
                lead_id, lead_first_name, lead_last_name, lead_company_name, 
                lead_official_title, lead_type, lead_generation_timestamp, 
                lead_generation_source, lead_status, lead_contact_number
            FROM {DB_SCHEMA}."lead"
            WHERE lead_status = :status_filter
            ORDER BY lead_id;
        """)

        result = db.execute(query, {"status_filter": "new"}).fetchall()
        
        # FastAPI will automatically convert the database rows to match the `Lead` Pydantic model
        return result
    except Exception as e:
        # Raise an HTTP exception if something goes wrong with the database query
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")