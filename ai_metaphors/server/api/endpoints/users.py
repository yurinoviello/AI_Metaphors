import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status

from ai_metaphors.server.api.api_key_manager import validate_api_key
from ai_metaphors.server.models.user import User
from ai_metaphors.server.schemas.user import UserCreate, UserOut

router = APIRouter(prefix="/users", tags=["users"])


def hash_password(password: str) -> str:
    # Use bcrypt directly to avoid passlib compatibility issues with newer bcrypt versions
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(validate_api_key)])
async def create_user(payload: UserCreate):
    # Check unique email
    existing = await User.get_by_email(payload.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = await User.create(
        email=payload.email,
        name=payload.name,
        password_hash=hash_password(payload.password),
        is_active=True,
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user")
    return user
