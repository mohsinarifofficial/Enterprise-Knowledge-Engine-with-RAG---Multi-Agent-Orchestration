import glob
import os
from datetime import datetime
from typing import List

from backend.config import settings
from backend.utils.hash import stable_hash
from backend.ingestion.pdf_loader import extract_text_per_page
from backend.ingestion.chunker import chunk_pages
from backend.retrieval.vector_store import PineconeStore

BATCH_SIZE = 200  # upsert in batches of records

def run_ingest():
    print("[Phase1] Starting ingestion (Pinecone integrated-embedding)...")
    store = PineconeStore(
        index_name=settings.pinecone_index,
        embed_model=settings.pinecone_embed_model,
        cloud=settings.pinecone_cloud,
        region=settings.pinecone_region
    )

    pdf_paths = glob.glob(settings.doc_glob, recursive=True)
    if not pdf_paths:
        print(f"No PDFs found at: {settings.doc_glob}")
        return

    for path in pdf_paths:
        doc_id = stable_hash(f"{path}::{os.path.getsize(path)}::{int(os.path.getmtime(path))}")
        pages = extract_text_per_page(path)
        chunks = chunk_pages(pages, settings.chunk_size, settings.chunk_overlap)

        # Build records for Pinecone upsert_records (records: list of dicts)
        records = []
        for c_idx, c in enumerate(chunks):
            record_id = stable_hash(doc_id + f"::{c['page']}::{c_idx}")
            rec = {
                "_id": record_id,
                "chunk_text": c["text"],   # this field will be embedded by Pinecone
                "source": path,
                "doc_id": doc_id,
                "page": c["page"],
                "chunk_index": c_idx,
                "char_len": len(c["text"]),
                "ingested_at": datetime.utcnow().isoformat() + "Z"
            }
            records.append(rec)

        # Upsert in batches
        for i in range(0, len(records), BATCH_SIZE):
            batch = records[i:i + BATCH_SIZE]
            print(f"Upserting batch {i//BATCH_SIZE + 1} ({len(batch)} records) from {os.path.basename(path)}")
            store.upsert_records(namespace=settings.namespace, records=batch)

    print("Ingestion complete")

if __name__ == "__main__":
    run_ingest()
