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
from app.views import AppViewSet

urlpatterns = [
    path(
        "qa/",
        AppViewSet.as_view({"get": "list", "post": "create"}),
        name="apps_list_ops",
    ),
    path("qa/<uuid:id>", AppViewSet.as_view({"get": "get_one"})),
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
