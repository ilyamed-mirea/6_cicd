from uuid import UUID, uuid4
from enum import Enum
from datetime import datetime
import uuid
from django.db import models


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


class Operation(models.Model):
    def __init__(self, id: UUID, result: bool = False) -> None:
        self.id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        self.created_at = models.DateTimeField(auto_now_add=True)
        self.updated_at = models.DateTimeField(auto_now=True)
        self.completed = models.BooleanField(default=False)
        self.result = models.TextField(null=True, blank=True)
