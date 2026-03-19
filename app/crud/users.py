from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.notes import User


def create_user(db: Session, user_data):
    stmt = select(User).where(User.email == user_data.email)
    user = db.scalars(stmt).first()

    if user:
        return user, False

    user = User(name=user_data.name, email=user_data.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user, True
