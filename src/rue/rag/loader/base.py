from abc import ABC, abstractmethod
from rue.rag.document import Document

class BaseLoader(ABC):
    @abstractmethod
    def load(self, source: str) -> list[Document]:
        pass