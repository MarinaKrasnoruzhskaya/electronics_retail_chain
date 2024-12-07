FROM python:3.12-alpine

# рабочая директория внутри проекта
WORKDIR /app

# переменные окружения для python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем зависимости для Postgre
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# устанавливаем зависимости
RUN pip install --upgrade pip
COPY /requirements.txt /
RUN pip install -r /requirements.txt --no-cache-dir

# копируем содержимое текущей папки в контейнер
COPY . .

ENTRYPOINT ["/app/entrypoint.sh"]
