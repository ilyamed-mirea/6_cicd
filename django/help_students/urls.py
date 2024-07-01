"""
URL configuration for help_students project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from app.views import (
    AddQAView,
    CompleteOperationView,
    CreateOperationView,
    ExportDataView,
    FinishOperationView,
    GetAnswerView,
    GetOperationInfoView,
    MostFrequentQuestionsView,
    GetQuestionsByUsersView,
    GetAllQAView,
)

urlpatterns = [
    path("all_qa/", GetAllQAView.as_view({"get": "list"}), name="all_qa"),
    path("add_qa/", AddQAView.as_view({"post": "create"}), name="all_qa"),
    path("get_answer/", GetAnswerView.as_view({"post": "create"}), name="get_answer"),
    path(
        "most_frequent_questions/",
        MostFrequentQuestionsView.as_view({"get": "list"}),
        name="most_frequent_questions",
    ),
    path(
        "get_questions_by_users/",
        GetQuestionsByUsersView.as_view({"get": "list"}),
        name="get_questions_by_users",
    ),
    path(
        "create_operation/",
        CreateOperationView.as_view({"post": "create"}),
        name="create_operation",
    ),
    path(
        "complete_operation/<int:operation_id>/",
        CompleteOperationView.as_view({"post": "create"}),
        name="complete_operation",
    ),
    path(
        "finish_operation/<int:operation_id>/",
        FinishOperationView.as_view({"post": "create"}),
        name="finish_operation",
    ),
    path(
        "get_operation_info/<int:operation_id>/",
        GetOperationInfoView.as_view({"get": "list"}),
        name="get_operation_info",
    ),
    path(
        "export_data/", ExportDataView.as_view({"post": "create"}), name="export_data"
    ),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
]

# Path: /api/qa
# Тип запроса: POST
# Авторизация: JWT
# Структура тела запроса:
# •	question (новый вопрос)
# •	message (ответ на новый вопрос)
# •	answer_file (ссылка на файл с доп. Информацией. опционально)
# Пример тела запроса:
# {
#     "question": "Тук-тук",
#     "message": "Кто там?"
# }
# Пример ответа:
# {"success": "true"}

# 2. Получение ответа на заданный вопрос
# Path: /api/qa
# Тип запроса: GET
# Авторизация: Отсутствует
# Структура параметров запроса:
# •	question (вопрос)
# Пример пути запроса:
# Path: /api/qa?question=”Тук-тук”
# Пример ответа:
# {
#     "message": "Кто там?"
# }

# 3. Получение самых популярных вопросов
# Path:  /api/stats/most_frequent
# Тип запроса: GET
# Авторизация: Отсутствует
# Структура параметров запроса:
# •	count (топ сколько запросов необходимо вернуть. опционально)
# Пример пути запроса:
# Path: /api/stats/most_frequent?count=2
# Пример ответа:
# {"data": ["Привет", "test"]}

# 4. Получение ответов пользователей
# Path:  /api/stats/questions_by_users
# Тип запроса: GET
# Авторизация: Отсутствует
# Пример ответа:
# {'test user': {'test', 'Привет'}, 'uisdhds232': {'Привет'}}
