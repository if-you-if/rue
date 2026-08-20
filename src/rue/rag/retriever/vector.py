
from rue.rag.embedding.base import BaseEmbedding
from rue.rag.retriever.base import BaseRetriever
from rue.rag.store.base import BaseVectorStore, SearchResult


class VectorRetriever(BaseRetriever):

    def __init__(self, embedding: BaseEmbedding, store: BaseVectorStore):
        self.embedding = embedding
        self.store = store
    
    def retrieve(self, query: str, top_k: int = 3) -> list[SearchResult]:
        query_embedding = self.embedding.embed(query)
        return self.store.search(query_embedding=query_embedding, top_k=top_k)