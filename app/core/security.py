import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status

password_hash = PasswordHash.recommended()

SECRET_KEY = "e586452d4da5e85e553048eb11b7df1c85c7eba4fc70e269fee93a4ded6310a2"
ALGORITHM = "HS256"
DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password: str):
    return password_hash.hash(password)


def verify_password(password: str, hash: str):
    return password_hash.verify(password, hash)


def create_access_token(data: dict, expire_minutes: int | None = None):
    to_encode = data.copy()
    if expire_minutes:
        expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except InvalidTokenError:
#         raise credentials_exception
#
#     user = get_user()
