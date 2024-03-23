from django.db import models
from uuid import UUID
from datetime import datetime
from typing_extensions import TypedDict


# class StatsTypes(Enum):
#     qa_frequency = "qa_frequency"
#     users_questions = "users_questions"

Stats = TypedDict(
    "Stats", {"qa_frequency": list[str], "users_questions": dict[UUID, list[str]]}
)


class Answer:
    message: str
    file: str | None

    def __init__(self, message: str, file: str | None = None) -> None:
        self.message = message
        self.file = file
