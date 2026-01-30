import os
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from lightrag import LightRAG, QueryParam
from lightrag.llm import openai_complete_if_cache, openai_embedding
from lightrag.utils import EmbeddingFunc
import numpy as np

app = FastAPI()

# Конфигурация из переменных окружения
WORKING_DIR = os.getenv("RAG_WORKING_DIR", "./rag_storage")
LLM_MODEL = os.getenv("LLM_MODEL", "deepseek/deepseek-r1-0528:free")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1")
LLM_API_KEY = os.getenv("LLM_API_KEY")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "qwen/qwen3-embedding-8b")
EMBEDDING_BASE_URL = os.getenv("EMBEDDING_BASE_URL", "https://openrouter.ai/api/v1")
EMBEDDING_API_KEY = os.getenv("EMBEDDING_API_KEY")

if not os.path.exists(WORKING_DIR):
    os.makedirs(WORKING_DIR)

# Функция эмбеддинга
async def embedding_func(texts: list[str]) -> np.ndarray:
    return await openai_embedding(
        texts,
        model=EMBEDDING_MODEL,
        base_url=EMBEDDING_BASE_URL,
        api_key=EMBEDDING_API_KEY
    )

# Инициализация LightRAG
# Примечание: Это базовая инициализация. 
# Настройте параметры по мере необходимости для вашей конкретной версии/использования LightRAG.
rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=openai_complete_if_cache,
    llm_model_name=LLM_MODEL,
    llm_model_max_async=4,
    llm_model_max_token_size=32768,
    llm_model_kwargs={
        "base_url": LLM_BASE_URL,
        "api_key": LLM_API_KEY
    },
    embedding_func=EmbeddingFunc(
        embedding_dim=1024, # Размерность для qwen/qwen3-embedding-8b, может потребоваться корректировка для других моделей
        max_token_size=8192,
        func=embedding_func
    )
)

class QueryRequest(BaseModel):
    query: str
    mode: str = "global" # "local", "global", "hybrid"

class IngestRequest(BaseModel):
    text: str

@app.post("/query")
async def query_rag(request: QueryRequest):
    try:
        # Сопоставление строкового режима с режимом LightRAG QueryParam
        # Это может потребовать корректировки в зависимости от точного API LightRAG
        result = rag.query(request.query, param=QueryParam(mode=request.mode))
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest")
async def ingest_text(request: IngestRequest):
    try:
        rag.insert(request.text)
        return {"status": "success", "message": "Text ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}
