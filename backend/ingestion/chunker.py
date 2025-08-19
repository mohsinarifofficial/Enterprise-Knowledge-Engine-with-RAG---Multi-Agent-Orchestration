from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_pages(pages: List[Dict], chunk_size: int, chunk_overlap: int) -> List[Dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", ".", " "]
    )
    chunks: List[Dict] = []
    for p in pages:
        for i, chunk in enumerate(splitter.split_text(p["text"])):
            chunks.append({
                "page": p["page"],
                "text": chunk,
                "chunk_index": i,
            })
    return chunks