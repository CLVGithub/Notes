from fastapi import APIRouter, HTTPException, Depends
from app.schemas.tags import Tag
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import tags as crud_tag

router = APIRouter(prefix="/api/v1/tags", tags=["tags"])


@router.delete("/{tag_id}", response_model=Tag)
async def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = crud_tag.delete_tag(db, tag_id)
    if not tag:
        raise HTTPException(
            status_code=404, detail=f"The tag with id {tag_id} does not exist."
        )
    return tag
