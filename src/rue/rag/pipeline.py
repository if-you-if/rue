from rue.rag.loader.base import BaseLoader
from rue.rag.splitter.base import TextSplitter
from rue.rag.embedding.base import BaseEmbedding
from rue.rag.store.base import BaseVectorStore,SearchResult
from rue.rag.retriever.base import BaseRetriever

class RAGPipeline:

    def __init__(
        self,
        loader: BaseLoader,
        splitter: TextSplitter,
        embedding: BaseEmbedding,
        store: BaseVectorStore,
        retriever: BaseRetriever,
    ):
        self.loader = loader
        self.splitter = splitter
        self.embedding = embedding
        self.store = store
        self.retriever = retriever
    
    def index(self, source: str) -> int:
        documents = self.loader.load(source)
        chunks = self.splitter.split(documents)
        embeddings = self.embedding.embed_batch([c.content for c in chunks])
        self.store.add(chunks, embeddings)
        return len(chunks)
    
    def retrieve(self, query: str, top_k: int = 3) -> list[SearchResult]:
        return self.retriever.retrieve(query, top_k=top_k)

    def retrieve_as_context(self, query: str, top_k: int = 3) -> str:
        results = self.retrieve(query, top_k=top_k)
        return "\n\n".join(
            f"[{i+1}]{r.chunk.content}" for i, r in enumerate(results)
        )