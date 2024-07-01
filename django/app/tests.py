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

    def test_get_all_QA(self):
        qa = self.qa_service.get_all_QA()
        self.assertIsInstance(qa, dict)
        self.assertIn("Привет", qa)
        self.assertIn("test", qa)

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
