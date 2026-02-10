from datetime import datetime, timedelta, timezone

import bcrypt
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from jose import JWTError, jwt

from ai_metaphors.server.models.user import User
from ai_metaphors.server.settings.settings import settings

# Authentication schemes
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login", auto_error=False)

# Use API_KEYS as the secret for JWT to avoid adding new settings
JWT_SECRET = settings.API_KEYS or "default-secret-for-dev-only"
JWT_ALGORITHM = "HS256"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User | None:
    if not token:
        return None

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
    except JWTError:
        return None

    user = await User.get(user_id)
    return user


async def unified_auth(
    api_key: str | None = Depends(api_key_header),
    current_user: User | None = Depends(get_current_user)
):
    """
    Dependency that allows access if either a valid API Key is provided 
    or a valid JWT token (logged in user) is provided.
    """
    # Check API Key
    if api_key and api_key in settings.VALID_API_KEYS:
        return True

    # Check JWT User
    if current_user:
        return True

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials. Provide a valid X-API-Key header or Bearer token.",
        headers={"WWW-Authenticate": "Bearer"},
    )
