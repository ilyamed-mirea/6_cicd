from pydantic import BaseModel


class Message(BaseModel):
    _id: str
    name: str

    # cover: str | None