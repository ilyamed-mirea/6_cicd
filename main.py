from typing import Union

from fastapi import FastAPI
from models.user import User
from models.message import Message

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/messages?msg={item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/messages/")
def add_message(new_message: Message):
    return {"item_name": item.name, "item_id": item_id}