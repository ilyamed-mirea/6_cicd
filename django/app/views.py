from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .services.qa import QAService
from .services.operations import OperationsService
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status

from .models import AnswerStatuses
from .serializers import (
    AddQASerializer,
    GetAnswerSerializer,
    MostFrequentQuestionsSerializer,
    GetQuestionsByUsersSerializer,
    OperationSerializer,
)

qa_service = QAService()


@extend_schema_view(
    list=extend_schema(
        summary="Получить все вопросы и ответы",
        description="Возвращает все вопросы и ответы в базе данных.",
        responses={200: "application/json"},
    )
)
class GetAllQAView(ViewSet):
    def list(self, request):
        qa_data = qa_service.get_all_QA()
        serialized_data = [
            {"question": question, "answer": answer.message}
            for question, answer in qa_data.items()
        ]
        return Response(serialized_data)


@extend_schema_view(
    create=extend_schema(
        summary="Добавить новый вопрос и ответ",
        description="Добавляет новый вопрос и ответ в базу данных.",
        request=AddQASerializer,
        responses={
            201: "application/json",
            400: "application/json",
        },
    )
)
class AddQAView(ViewSet):
    def create(self, request):
        serializer = AddQASerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            success = qa_service.add_QA(
                validated_data["question"],
                validated_data["answer_message"],
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


@extend_schema_view(
    create=extend_schema(
        summary="Получить ответ на вопрос",
        description="Возвращает ответ на заданный вопрос для конкретного пользователя.",
        request=GetAnswerSerializer,
        responses={
            200: "application/json",
            404: "application/json",
            400: "application/json",
        },
    )
)
class GetAnswerView(ViewSet):
    def create(self, request):
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
                        "status": answer.status.name,
                    }
                )
            else:
                return Response(
                    {"message": "Answer not found"}, status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=extend_schema(
        summary="Получить наиболее часто задаваемые вопросы",
        description="Возвращает наиболее часто задаваемые вопросы.",
        responses={200: "application/json"},
    )
)
class MostFrequentQuestionsView(ViewSet):
    def list(self, request):
        serializer = MostFrequentQuestionsSerializer(data=request.query_params)
        if serializer.is_valid():
            return_count = serializer.validated_data["return_count"]
            questions = qa_service.get_most_frequent_questions(return_count)
            return Response({"questions": questions})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=extend_schema(
        summary="Получить вопросы по пользователям",
        description="Возвращает вопросы, заданные пользователями в заданном файле.",
        responses={200: "application/json"},
    )
)
class GetQuestionsByUsersView(ViewSet):
    def list(self, request):
        serializer = GetQuestionsByUsersSerializer(data=request.query_params)
        if serializer.is_valid():
            filename = serializer.validated_data["filename"]
            user_questions = qa_service.get_questions_by_users(filename)
            return Response({"user_questions": user_questions})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


operation_service = OperationsService()


@extend_schema_view(
    create=extend_schema(
        summary="Создание новой операции",
        description="Создает новую операцию и возвращает ее данные.",
        responses={201: OperationSerializer},
    )
)
class CreateOperationView(ViewSet):
    def create(self, request):
        operation = operation_service.create_operation()
        serializer = OperationSerializer(operation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema_view(
    create=extend_schema(
        summary="Завершение операции",
        description="Завершает указанную операцию с предоставленным результатом.",
        request={"result": "string"},
        responses={
            200: OperationSerializer,
            404: "application/json",
        },
    )
)
class CompleteOperationView(ViewSet):
    def create(self, request, operation_id):
        result = request.data.get("result", "")
        operation = operation_service.complete_operation(operation_id, result)
        if operation:
            serializer = OperationSerializer(operation)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"detail": "Operation not found"}, status=status.HTTP_404_NOT_FOUND
        )


@extend_schema_view(
    create=extend_schema(
        summary="Завершение операции без результата",
        description="Завершает указанную операцию без предоставления результата.",
        responses={
            200: OperationSerializer,
            404: "application/json",
        },
    )
)
class FinishOperationView(ViewSet):
    def create(self, request, operation_id):
        operation = operation_service.finish_operation(operation_id)
        if operation:
            serializer = OperationSerializer(operation)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"detail": "Operation not found"}, status=status.HTTP_404_NOT_FOUND
        )


@extend_schema_view(
    list=extend_schema(
        summary="Получить информацию об операции",
        description="Возвращает информацию о конкретной операции.",
        responses={
            200: OperationSerializer,
            404: "application/json",
        },
    )
)
class GetOperationInfoView(ViewSet):
    def list(self, request, operation_id):
        operation = operation_service.get_operation_info(operation_id)
        if operation:
            serializer = OperationSerializer(operation)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"detail": "Operation not found"}, status=status.HTTP_404_NOT_FOUND
        )


@extend_schema_view(
    create=extend_schema(
        summary="Экспорт данных",
        description="Запускает процесс экспорта данных.",
        responses={
            201: OperationSerializer,
        },
    )
)
class ExportDataView(ViewSet):
    def create(self, request):
        operation = qa_service.export_data()
        serializer = OperationSerializer(operation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
