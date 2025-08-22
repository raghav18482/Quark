"""User-related routes (protected)."""
from fastapi import APIRouter, Depends

from ..schemas import UserOut
from ..security import get_current_user
from ..models import User


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
	"""Return the authenticated user resolved from the Authorization Bearer token."""
	return current_user
