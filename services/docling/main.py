from fastapi import FastAPI, UploadFile, File, HTTPException
from docling.document_converter import DocumentConverter
import tempfile
import os
import shutil

app = FastAPI()
converter = DocumentConverter()

@app.post("/convert")
async def convert_document(file: UploadFile = File(...)):
    try:
        # Создание временного файла для сохранения загруженного контента
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        try:
            # Конвертация документа
            result = converter.convert(tmp_path)
            # Экспорт в markdown
            markdown_output = result.document.export_to_markdown()
            return {"markdown": markdown_output}
        finally:
            # Очистка временного файла
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}
