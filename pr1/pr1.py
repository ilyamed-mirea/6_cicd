import enum
from uuid import UUID, uuid4
from datetime import datetime
class ApplicationStatuses(enum.Enum):
    CANCELED = -1 # Заявка отменена
    CREATED = 0 # Заявка создана

class App:
    def __init__(self) -> None:
        self.faq = {}

    # Создание заявки
    def create_application(user_id: UUID, start: str, destintion: str) -> Application:
        application = Application(user_id, start, destintion)
        applications.append(application)
        return application