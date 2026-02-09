FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей при необходимости (например, для библиотек обработки PDF)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка docling
RUN pip install --no-cache-dir docling uvicorn fastapi python-multipart

# Копирование кода приложения
COPY . .

# Открытие порта
EXPOSE 8000

# Запуск приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
