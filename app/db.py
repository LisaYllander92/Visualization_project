import os
from sqlalchemy import create_engine
from dotenv import load_dotenv


# Load variables from the .env file (POSTGRES_HOST, POSTGRES_USER, etc.)
load_dotenv()


def get_engine():
    """
    Build and return a SQLAlchemy database engine using .env credentials.

    SQLAlchemy is the library that lets Python talk to PostgreSQL.
    The 'engine' is essentially the connection object we pass around.
    """
    host     = os.getenv("POSTGRES_HOST", "localhost")
    port     = os.getenv("POSTGRES_PORT", "5432")
    database = os.getenv("POSTGRES_DB",   "events_db")
    user     = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "densen")

    # Build the connection string in the format SQLAlchemy expects:
    # postgresql+psycopg2://user:password@host:port/database
    connection_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

    return create_engine(connection_url)
