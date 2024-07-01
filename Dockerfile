FROM python:3.10-slim

WORKDIR /app

COPY ./django/requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY ./django .

RUN python manage.py migrate

COPY ./entry.sh .
RUN chmod 777 entry.sh
ENTRYPOINT ["./entry.sh"]