"""Database bootstrap: SQLAlchemy engine, session factory, and FastAPI dependency."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import settings


# Create SQLAlchemy engine; pass sqlite-specific connect_args when using SQLite
engine = create_engine(
	settings.database_url,
	connect_args={"check_same_thread": False} if settings.database_url.startswith("sqlite") else {},
)
# Session factory used to create per-request DB sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base for ORM models
Base = declarative_base()


def get_db():
	"""FastAPI dependency that yields a request-scoped DB session."""
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
