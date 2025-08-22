"""Pydantic schemas for request validation and response serialization."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
	"""Payload to create/register a user."""
	email: EmailStr
	password: str


class UserOut(BaseModel):
	"""Public user shape returned by the API."""
	id: int
	email: EmailStr
	is_active: bool
	created_at: datetime

	class Config:
		# Enable ORM mode (Pydantic v2): allow from SQLAlchemy model instances
		from_attributes = True


class Token(BaseModel):
	"""Access token response payload."""
	access_token: str
	token_type: str


class TokenData(BaseModel):
	"""Decoded token data used internally."""
	sub: Optional[str] = None
