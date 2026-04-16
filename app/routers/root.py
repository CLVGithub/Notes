from fastapi import APIRouter, HTTPException, Depends, status

# root path for testing
router = APIRouter(tags=["root"])


@router.get("/", summary="Root path for testing")
async def read_root():
    return {"somekey": "This is the root"}
