from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel

class Note(BaseModel):
    title: str
    content: str
    tags: list[str] 


class Sort(str, Enum):
    created_at = 'created_at'
    updated_at = 'updated_at'

app = FastAPI()

items = [Note(title='Food', content='I love these kinds of foods', tags=['food', 'health', 'exercise']),
         Note(title='Study', content='Need to study these chapters.', tags=['university', 'books']),
         Note(title='Laundry', content='These are the detergents to use and the method to follow.', tags=['chores', 'clothes'])]

@app.get('/hello')
async def hello():
    return 'Hello World'

@app.get('/items/{item_id}')
async def get_item(item_id: int):
    return items[item_id]

@app.get('/search')
async def search(q: str, sort: Sort = Sort('updated_at'), skip: int = 0, limit: int = 2):
    return {
        'query': q,
        'items': items[skip: skip + limit],
        'sort': sort
    }

@app.post('/notes', response_model=Note)
async def post_notes(note: Note):
    items.append(Note(title=note.title, content=note.content, tags=note.tags))
    return Note(title=note.title, content=note.content, tags=note.tags)

@app.get('/notes')
async def get_notes():
    return items
