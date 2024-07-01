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
    status: AnswerStatuses

    def __init__(
        self,
        message: str,
        status=AnswerStatuses.CREATED,
    ) -> None:
        self.id = uuid4()
        self.creation_date = datetime.now()
        self.message = message
        self.status = status


class Operation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    result = models.TextField(null=True, blank=True)

    def init(self, result: bool = False) -> None:
        super().init()
        self.id = uuid.uuid4()
        self.result = result
