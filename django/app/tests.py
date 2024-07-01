from uuid import uuid4
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from app.services.qa import QAService
from app.services.operations import OperationsService

client = APIClient()


class QAServiceTestCase(TestCase):
    def setUp(self):
        self.qa_service = QAService()

    def test_add_qa(self):
        result = self.qa_service.add_QA("New Question", "New Answer")
        self.assertTrue(result)
        self.assertIn("New Question", self.qa_service.get_all_QA())

    def test_get_answer(self):
        self.qa_service.add_QA("Test Question", "Test Answer")
        answer = self.qa_service.get_answer("Test Question")
        self.assertEqual(answer.message, "Test Answer")

    def test_get_most_frequent_questions(self):
        self.qa_service.add_QA("Q1", "A1")
        self.qa_service.add_QA("Q2", "A2")
        self.qa_service.get_answer("Q1")
        self.qa_service.get_answer("Q1")
        self.qa_service.get_answer("Q2")
        frequent_questions = self.qa_service.get_most_frequent_questions(2)
        self.assertEqual(frequent_questions, ["Q1", "Q2"])


class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.qa_service = QAService()
        self.operations_service = OperationsService()

    def test_get_all_qa(self):
        url = reverse("all_qa")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_qa(self):
        url = reverse("all_qa")
        data = {
            "question": "New API Question",
            "answer_message": "New API Answer",
            "answer_status": "Created",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_answer(self):
        self.qa_service.add_QA("API Question", "API Answer")
        url = reverse("get_answer")
        data = {"question": "API Question", "user_id": str(uuid4())}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "API Answer")

    def test_most_frequent_questions(self):
        url = reverse("most_frequent_questions")
        response = self.client.get(url, {"return_count": 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_operation(self):
        url = reverse("create_operation")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_complete_operation(self):
        operation = self.operations_service.create_operation()
        url = reverse("complete_operation", args=[operation.id])
        data = {"result": "Completed"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_export_data(self):
        url = reverse("export_data")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
