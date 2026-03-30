from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.users import User
from app.core.security import hash_password


def create_user(db: Session, user_data):
    stmt = select(User).where(User.email == user_data.email)
    user = db.scalars(stmt).first()

    if user:
        return user, False

    user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user, True


def get_user(db: Session, email: str):
    stmt = select(User).where(User.email == email)
    user = db.scalars(stmt).first()

    return user
