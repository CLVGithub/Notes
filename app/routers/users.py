from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas.users import UserCreate, UserResponse
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.crud import users as crud_user

router = APIRouter(prefix="/users", tags=["users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    response = crud_user.create_user(db, user)
    user_database, created = response
    if not created:
        raise HTTPException(
            status_code=409,
            detail=f"A user with that email already exists:  {user_database}",
        )

    return user_database
