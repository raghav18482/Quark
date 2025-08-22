"""SQLAlchemy ORM models."""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func

from .database import Base


class User(Base):
	"""User account record."""
	__tablename__ = "users"  # DB table name

	id = Column(Integer, primary_key=True, index=True)
	email = Column(String, unique=True, index=True, nullable=False)
	hashed_password = Column(String, nullable=False)
	is_active = Column(Boolean, default=True, nullable=False)
	created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
