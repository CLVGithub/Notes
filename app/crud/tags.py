from sqlalchemy.orm import Session
from app.models import Tag


def delete_tag(db: Session, tag_id: int):
    tag = db.get(Tag, tag_id)
    if tag:
        db.delete(tag)
        db.commit()
    return tag
