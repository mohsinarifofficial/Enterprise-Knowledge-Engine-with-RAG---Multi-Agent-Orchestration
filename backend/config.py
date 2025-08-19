from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    pinecone_api_key: str = os.getenv("PINECONE_API_KEY", "")
    pinecone_cloud: str = os.getenv("PINECONE_CLOUD", "aws")
    pinecone_region: str = os.getenv("PINECONE_REGION", "us-east-1")
    pinecone_index: str = os.getenv("PINECONE_INDEX_NAME", "enterprise-knowledge")
    pinecone_embed_model: str = os.getenv("PINECONE_EMBED_MODEL", "llama-text-embed-v2")

    chunk_size: int = int(os.getenv("CHUNK_SIZE", "800"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "120"))
    doc_glob: str = os.getenv("DOC_GLOB", "./docs/**/*.pdf")
    namespace: str = os.getenv("NAMESPACE", "default")

settings = Settings()
