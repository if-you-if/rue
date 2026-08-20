from abc import ABC, abstractmethod
from dataclasses import dataclass
from rue.rag.chunk import Chunk


@dataclass
class SearchResult:
    chunk: Chunk
    score: float

class BaseVectorStore(ABC):
    @abstractmethod
    def add(self, chunks: list[Chunk], embedding: list[list[float]]) -> None:
        pass

    def search(self, query_embedding: list[float], top_k: int = 3) -> list[SearchResult]:
        pass
