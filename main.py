from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends

app = FastAPI()

def common_parameters(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.get("/users/")
def read_users(commons: dict = Depends(common_parameters)):
    return commons

@app.get("/books/")
def read_books(commons: dict = Depends(common_parameters)):
    return commons




class ItemCreate(BaseModel):
    name: str
    price: float
    is_available: bool = True

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    is_available: bool

@app.post("/items/", response_model=ItemResponse)
def create_item(item: ItemCreate):
    return {"id": 1, "name": item.name, "price": item.price, "is_available": item.is_available}

fake_db = {1: {"id": 1, "name": "本", "price": 1500.0, "is_available": True}}

@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, q: Optional[str] = None):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]

