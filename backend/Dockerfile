# Используем легковесный и безопасный образ Python 3.11
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Отключаем создание файлов .pyc и включаем немедленный вывод логов (unbuffered)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Копируем сначала только requirements.txt
# Это оптимизирует кеш Docker: если зависимости не менялись, этот слой не будет пересобираться
COPY requirements.txt .

# Обновляем pip и устанавливаем зависимости без кеширования
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Копируем весь исходный код приложения
COPY ./app /app/app

# Создаем непривилегированного пользователя для безопасности (Security Best Practice)
RUN useradd -m apiuser \
    && chown -R apiuser:apiuser /app
USER apiuser

# Открываем порт
EXPOSE 8000

# Команда запуска FastAPI сервера через Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]