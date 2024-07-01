from datetime import datetime
from sched import scheduler
from typing import Optional, TypedDict
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger

# import time
from uuid import UUID, uuid4

# from datetime import datetime
from app.models import Answer
from app.services.operations import OperationsService

Stats = TypedDict(
    "Stats", {"qa_frequency": list[str], "users_questions": dict[UUID, list[str]]}
)


class QAService:
    _QA: dict[str, Answer]
    _stats: Stats

    def __init__(self) -> None:
        self._QA = {"Привет": Answer("Привет и тебе"), "test": Answer("test test")}
        self._stats = {
            "qa_frequency": {},
            "users_questions": {},
        }
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.operations_service = OperationsService()

    def get_all_QA(self):
        return self._QA

    def add_QA(
        self,
        question: str,
        answer_message: str,
        answer_status: Optional[str] = None,
    ) -> bool:
        if question in self._QA:
            return False
        self._QA[question] = Answer(answer_message, answer_status)
        return True

    def get_answer(self, question: str, user_id: UUID = "test") -> Answer:
        if question in self._QA:
            answer = self._QA[question]
            self._stats["qa_frequency"][question] = (
                self._stats["qa_frequency"].get(question, 0) + 1
            )
            user_question_set: set[str] = self._stats["users_questions"].get(
                user_id, set()
            )
            user_question_set.add(question)
            self._stats["users_questions"][user_id] = user_question_set
            return answer
        else:
            # raise Exception("Произошла ошибка при получении ответа!")
            return "Произошла ошибка!"

    def get_most_frequent_questions(self, return_count: int = 10):
        freq_items = self._stats["qa_frequency"].items()
        frequency = [[] for _ in range(len(freq_items) + 1)]
        for question, count in freq_items:
            frequency[count].append(question)
        res = []
        for questions in reversed(frequency):
            for question in questions:
                res.append(question)
                return_count -= 1
                if return_count == 0:
                    return res
        return res

    def get_questions_by_users(self, filename: str = "./export.txt"):
        with open(filename, "w") as file:
            for user, questions in self._stats["users_questions"].items():
                file.write(f"{user}: {questions}\n")

        return self._stats["users_questions"]

    def _applications_to_file(self, operation_id):
        filename = f"applications_{operation_id}.txt"
        with open(filename, "w") as file:
            for question, answer in self._QA.items():
                file.write(f"Question: {question}\nAnswer: {answer.message}\n\n")

        self.operations_service.finish_operation(operation_id, {"url": filename})

    def export_data(self):
        operation = self.operations_service.create_operation()

        scheduler.add_job(
            self._applications_to_file,
            DateTrigger(datetime.now()),
            run_date=None,
            args=(str(operation.id),),
        )

        return operation
