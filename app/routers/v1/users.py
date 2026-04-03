from fastapi import APIRouter, HTTPException, Depends
from app.core.security import verify_password, create_access_token
from app.schemas.users import UserCreate, UserResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import users as crud_user

from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    response = crud_user.create_user(db, user)
    user_database, created = response
    if not created:
        raise HTTPException(
            status_code=409,
            detail=f"A user with that email already exists:  {user_database}",
        )

    return user_database


@router.post("/login")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = crud_user.get_user(db, form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    print("Found user")
    print(user)  # this should be in repr form

    access_token = create_access_token({"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}
