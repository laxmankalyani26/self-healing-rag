from fastapi import FastAPI, UploadFile, File
import shutil

from app.models.chat_models import ChatRequest
from app.services.rag_service import RAGService
from app.services.ingestion_service import IngestionService


app = FastAPI()


rag_service = RAGService()

ingestion_service = IngestionService()


@app.get("/")
def health_check():

    return {
        "status": "running"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    response = rag_service.ask_question(
        request.query,
        request.chat_history
    )

    return response


@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):

    file_path = f"data/{file.filename}"

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(file.file, buffer)

    file_hash = ingestion_service.generate_file_hash(
        file_path
    )

    if ingestion_service.document_exists(file_hash):

        return {
            "message": "Document already uploaded",
            "file_hash": file_hash
        }

    chunks_created = ingestion_service.ingest_pdf(
        file_path
    )

    ingestion_service.register_document(
        file.filename,
        file_hash,
        chunks_created
    )

    return {
        "message": "PDF uploaded successfully",
        "filename": file.filename,
        "file_hash": file_hash,
        "chunks_created": chunks_created
    }