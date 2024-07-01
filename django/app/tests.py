from uuid import uuid4
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from .models import AnswerStatuses, Operation
from .services import QAService

client = APIClient()


class QuestionAnswerTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.question = "Как дела?"
        cls.answer_message = "Все хорошо"
        cls.answer_status = AnswerStatuses.CREATED

        cls.qa_service = QAService()
        cls.qa_service.add_QA(cls.question, cls.answer_message, cls.answer_status)

    def test_add_qa(self):
        url = reverse("add_qa")
        data = {
            "question": "Какой твой любимый цвет?",
            "answer_message": "Синий",
            "answer_status": AnswerStatuses.CREATED,
        }
        response = client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Question added successfully")

    def test_add_qa_existing_question(self):
        url = reverse("add_qa")
        data = {
            "question": self.question,
            "answer_message": self.answer_message,
            "answer_status": self.answer_status,
        }
        response = client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Question already exists")

    def test_get_answer(self):
        url = reverse("get_answer")
        data = {"question": self.question, "user_id": uuid4()}
        response = client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], self.answer_message)
        self.assertEqual(response.data["status"], self.answer_status.name)

    def test_get_answer_non_existing_question(self):
        url = reverse("get_answer")
        data = {"question": "Несуществующий вопрос", "user_id": uuid4()}
        response = client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "Answer not found")

    def test_most_frequent_questions(self):
        url = reverse("most_frequent_questions")
        response = client.get(url, data={"return_count": 10})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.question, response.data["questions"])

    def test_get_questions_by_users(self):
        url = reverse("user_questions")
        response = client.get(url, data={"filename": "export.txt"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data["user_questions"], dict)

    def test_get_all_qa(self):
        url = reverse("all_qa")
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(qa["question"] == self.question for qa in response.data))


class OperationTests(APITestCase):
    def test_create_operation(self):
        url = reverse("create_operation")
        response = client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue("id" in response.data)

    def test_complete_operation(self):
        operation = Operation.objects.create()
        url = reverse("complete_operation", args=[operation.id])
        data = {"result": "Operation completed successfully"}
        response = client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["completed"])
        self.assertEqual(response.data["result"], "Operation completed successfully")

    def test_finish_operation(self):
        operation = Operation.objects.create()
        url = reverse("finish_operation", args=[operation.id])
        response = client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["completed"])
        self.assertIsNone(response.data["result"])

    def test_get_operation_info(self):
        operation = Operation.objects.create()
        url = reverse("get_operation_info", args=[operation.id])
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(operation.id))
