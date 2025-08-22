"""Security utilities: password hashing, JWT creation/verification, and auth dependencies."""
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .config import settings
from .database import get_db
from .models import User


# Configure Passlib for bcrypt hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# OAuth2 "password" flow token provider mounted at /auth/login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
	"""Return True if the plain password matches the stored bcrypt hash."""
	return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
	"""Hash a password for storing using bcrypt."""
	return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
	"""Create a signed JWT with expiration (exp claim)."""
	to_encode = data.copy()
	expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
	return encoded_jwt


def get_user_by_email(db: Session, email: str) -> Optional[User]:
	"""Fetch a user by email or return None."""
	return db.query(User).filter(User.email == email).first()


def get_current_user(
	token: str = Depends(oauth2_scheme),
	db: Session = Depends(get_db),
) -> User:
	"""Resolve and return the current authenticated user from the Bearer token.

	Raises 401 if token is invalid/expired or user no longer exists.
	"""
	credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Could not validate credentials",
		headers={"WWW-Authenticate": "Bearer"},
	)
	try:
		payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
		email: Optional[str] = payload.get("sub")
		if email is None:
			raise credentials_exception
	except JWTError:
		raise credentials_exception
	user = get_user_by_email(db, email)
	if user is None:
		raise credentials_exception
	return user
