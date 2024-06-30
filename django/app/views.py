from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.exceptions import ValidationError
from .services.qa import QAService

from rest_framework import status
from rest_framework.views import APIView

from .models import AnswerStatuses
from .serializers import (
    AddQASerializer,
    GetAnswerSerializer,
    MostFrequentQuestionsSerializer,
    GetQuestionsByUsersSerializer,
    OperationSerializer,
)

qa_service = QAService()


class GetAllQAView(APIView):
    def get(self, request):
        qa_data = qa_service.get_all_qa()
        serialized_data = [
            {"question": question, "answer": answer}
            for question, answer in qa_data.items()
        ]
        return Response(serialized_data)


class AddQAView(APIView):
    def post(self, request):
        serializer = AddQASerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            success = qa_service.add_QA(
                validated_data["question"],
                validated_data["answer_message"],
                validated_data.get("answer_file"),
                validated_data["answer_status"],
            )
            if success:
                return Response(
                    {"message": "Question added successfully"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"message": "Question already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAnswerView(APIView):
    def post(self, request):
        serializer = GetAnswerSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            answer = qa_service.get_answer(
                validated_data["question"], validated_data["user_id"]
            )
            if answer.status == AnswerStatuses.CREATED:
                return Response(
                    {
                        "message": answer.message,
                        "file": answer.file,
                        "status": answer.status.name,
                    }
                )
            else:
                return Response(
                    {"message": "Answer not found"}, status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MostFrequentQuestionsView(APIView):
    def get(self, request):
        serializer = MostFrequentQuestionsSerializer(data=request.query_params)
        if serializer.is_valid():
            return_count = serializer.validated_data["return_count"]
            questions = qa_service.get_most_frequent_questions(return_count)
            return Response({"questions": questions})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetQuestionsByUsersView(APIView):
    def get(self, request):
        serializer = GetQuestionsByUsersSerializer(data=request.query_params)
        if serializer.is_valid():
            filename = serializer.validated_data["filename"]
            user_questions = qa_service.get_questions_by_users(filename)
            return Response({"user_questions": user_questions})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OperationView(APIView):
    def post(self, request):
        serializer = OperationSerializer(data=request.data)
        if serializer.is_valid():
            # Here you would tie this into a real operation
            validated_data = serializer.validated_data
            # Simulate operation result
            operation = serializer.create(validated_data)
            return Response(
                {"id": operation.id, "done": operation.done, "result": operation.result}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
