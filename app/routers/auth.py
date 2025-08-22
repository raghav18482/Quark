"""Authentication routes: user registration and token issuance (login)."""
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserOut, Token
from ..security import get_password_hash, verify_password, create_access_token


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
	"""Create a new user with a hashed password.

	Returns the created user (public fields only). 400 if email already exists.
	"""
	existing = db.query(User).filter(User.email == payload.email).first()
	if existing:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
	user = User(
		email=payload.email,
		hashed_password=get_password_hash(payload.password),
	)
	db.add(user)
	db.commit()
	db.refresh(user)
	return user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	"""Issue a JWT if the provided credentials are valid.

	Uses OAuth2 password flow form fields (username=email, password=...). Returns
	{"access_token", "token_type"} on success, 401 on failure.
	"""
	user = db.query(User).filter(User.email == form_data.username).first()
	if not user or not verify_password(form_data.password, user.hashed_password):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
	token_expires = timedelta(minutes=60)
	token = create_access_token({"sub": user.email}, expires_delta=token_expires)
	return {"access_token": token, "token_type": "bearer"}
