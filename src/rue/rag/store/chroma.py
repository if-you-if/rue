import chromadb
from rue.rag.store.base import BaseVectorStore, SearchResult
from rue.rag.chunk import Chunk
from pathlib import Path


class ChromaVectorStore(BaseVectorStore):

    def __init__(self, collection_name: str = "rue_docs", persist_dir: str | None = None):
        base = persist_dir or settings.vector_db_path
        path = Path(base)
        self.persist_dir = str(path if path.is_absolute() else PROJECT_ROOT / path)
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def add(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        ids = [f"chunk_{i}" for i in range(self.collection.count(), self.collection.count() + len(chunks))]
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=[chunk.content for chunk in chunks],
            metadatas=[chunk.metadata for chunk in chunks]
        )

    def search(self, query_embedding: list[float], top_k: int = 3) -> list[SearchResult]:
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        search_results = []
        for i in range(len(results["ids"][0])):
            chunk = Chunk(
                content=results["documents"][0][i],
                metadata=results["metadatas"][0][i],
            )
            score = 1.0 - results["distances"][0][i]
            search_results.append(SearchResult(chunk=chunk, score=score))
        return search_results
    
    def clear(self) -> None:
        """清空 collection 中的所有数据"""
        if self.collection.count() > 0:
            self.collection.delete(ids=self.collection.get()["ids"])
    

