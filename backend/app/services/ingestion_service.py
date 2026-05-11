import os
import hashlib
import json
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


class IngestionService:

    def __init__(self):

        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.vector_db = Chroma(
            persist_directory="backend/vectorstore",
            embedding_function=self.embedding_model
        )

        self.upload_dir = "backend/data"

        os.makedirs(self.upload_dir, exist_ok=True)
        self.registry_path = "data/documents.json"
    def generate_file_hash(self, file_path):

        hasher = hashlib.md5()

        with open(file_path, "rb") as file:

            buffer = file.read()

            hasher.update(buffer)

        return hasher.hexdigest()
    
    def load_registry(self):

        with open(self.registry_path, "r") as file:

            return json.load(file)


    def save_registry(self, registry):

        with open(self.registry_path, "w") as file:

            json.dump(registry, file, indent=4)


    def document_exists(self, file_hash):

        registry = self.load_registry()

        for document in registry:

            if document["file_hash"] == file_hash:

                return True

        return False


    def register_document(
        self,
        filename,
        file_hash,
        chunks_created
    ):

        registry = self.load_registry()

        registry.append({
            "filename": filename,
            "file_hash": file_hash,
            "chunks_created": chunks_created
        })

        self.save_registry(registry)

    def ingest_pdf(self, file_path):

        loader = PyPDFLoader(file_path)

        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        chunks = text_splitter.split_documents(documents)

        self.vector_db.add_documents(chunks)

        return len(chunks)