# import enum
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional


class Answer:
    def __init__(self, message: str, file: Optional[str] = None) -> None:
        self.message = message
        self.file = file

    def __str__(self):
        return self.message


class App:
    def __init__(self) -> None:
        self._QA = {"Привет": Answer("Привет и тебе"), "test": Answer("test test")}
        self._stats = {
            "qa_frequency": {},
            "users_questions": {},
        }

    def add_QA(
        self, question: str, answer_message: str, answer_file: Optional[str] = None
    ) -> bool:
        if question in self._QA:
            return False
        self._QA[question] = Answer(answer_message, answer_file)
        return True

    def get_answer(self, question: str, user_id: str = "test user") -> Answer:
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


app = App()
print(app.get_answer("Привет"))
print(app.get_answer("Привет", "uisdhds232"))
print(app.get_answer("test"))
print(app.get_most_frequent_questions())
print(app.get_questions_by_users())
