from abc import ABC, abstractmethod
from rue.rag.store.base import SearchResult


class BaseRetriever(ABC):
    @abstractmethod
    def retrieve(self, query: str, top_k: int = 3) -> list[SearchResult]:
        pass
    