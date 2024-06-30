from uuid import UUID, uuid4
from enum import Enum
from datetime import datetime


class AnswerStatuses(Enum):
    CREATED = 0
    PROCESSING = 1
    FINISHED = 2


class Answer:
    id: UUID
    creation_date: datetime
    message: str
    file: str | None
    status: AnswerStatuses

    def __init__(
        self,
        message: str,
        file: str | None = None,
        status=AnswerStatuses.CREATED,
    ) -> None:
        self.id = uuid4()
        self.creation_date = datetime.now()
        self.message = message
        self.file = file
        self.status = status


class Operation:
    id: UUID
    done: bool

    def __init__(self, id: UUID, done: bool = False, result=None) -> None:
        self.id = id
        self.done = done
        self.result = result
