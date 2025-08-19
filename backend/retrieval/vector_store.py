import os
from typing import List, Dict, Optional
from pinecone import Pinecone, ServerlessSpec

class PineconeStore:
    """
    Minimal wrapper using Pinecone integrated-embedding index.
    - Creates index_for_model(name, embed={"model":..., "field_map": {"text": "chunk_text"}})
    - Upserts records via index.upsert_records(namespace, records)
    """

    def __init__(self, index_name: str, embed_model: str, cloud: str = "aws", region: str = "us-east-1"):
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index_name = index_name
        self.embed_model = embed_model
        self.cloud = cloud
        self.region = region

        # Create integrated index if missing (server-side embedding)
        if not self.pc.has_index(index_name):
            self.pc.create_index_for_model(
                name=index_name,
                cloud=self.cloud,
                region=self.region,
                embed={
                    "model": self.embed_model,
                    # map model input field "text" to our document field "chunk_text"
                    "field_map": {"text": "chunk_text"}
                }
            )
        # Instantiate index client
        self.index = self.pc.Index(index_name)

    def upsert_records(self, namespace: str, records: List[Dict]):
        """
        Upsert text records.
        Each record is a dict like:
          {
            "_id": "my-id",
            "chunk_text": "document text to be embedded",
            "source": "path/or/url",
            "page": 3,
            ...
          }
        Pinecone will convert 'chunk_text' -> vectors automatically for integrated indexes.
        """
        if not records:
            return
        # Upsert in one call. If you have huge batches, batch them yourself.
        # signature: index.upsert_records(namespace, [record, record, ...])
        self.index.upsert_records(namespace, records)

    def search_text(self, namespace: str, query_text: str, top_k: int = 5, fields: Optional[List[str]] = None, rerank: Optional[Dict] = None):
        """
        Search with a query text (supported only for integrated-embedding indexes).
        returns Pinecone response (dict-like).
        """
        query = {"inputs": {"text": query_text}, "top_k": top_k}
        return self.index.search(namespace=namespace, query=query, fields=fields, rerank=rerank)

    def delete_namespace(self, namespace: str):
        """Utility: delete all records in a namespace (useful for re-ingest during testing)."""
        self.index.delete_namespace(namespace)
