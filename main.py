from fastapi import FastAPI
from routers.notes import router as notes_router


app = FastAPI(title="Notes API")

app.include_router(notes_router)
