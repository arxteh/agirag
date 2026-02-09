FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка LightRAG и зависимостей
# Примечание: LightRAG может потребовать специфических шагов установки в зависимости от точной версии библиотеки/источника
# Предполагается стандартный пакет pip или requirements
RUN pip install --no-cache-dir lightrag-hku==1.4.9.9 uvicorn fastapi qdrant-client openai

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
