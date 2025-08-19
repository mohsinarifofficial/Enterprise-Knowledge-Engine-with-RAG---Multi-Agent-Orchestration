from backend.config import settings
from backend.retrieval.vector_store import PineconeStore

def quick_search(q: str, k: int = 5):
    store = PineconeStore(index_name=settings.pinecone_index, embed_model=settings.pinecone_embed_model,
                          cloud=settings.pinecone_cloud, region=settings.pinecone_region)
    resp = store.search_text(namespace=settings.namespace, query_text=q, top_k=k, fields=["chunk_text", "source", "page"])
    # print results
    # print(resp)
    for r in resp.get("result", {}).get("hits", []):
        print(f"score={r.get('_score')}, id={r.get('_id')}, src={r.get('fields', {}).get('source')}")
        print(r.get("fields", {}).get("chunk_text", "")[:300])
        print("----")

if __name__ == "__main__":
    quick_search("What initiatives are planned to improve customer engagement?", 5)
