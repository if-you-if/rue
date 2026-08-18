from abc import ABC, abstractmethod
from dataclasses import dataclass
from .document import Document

class BaseLoader(ABC):
    @abstractmethod
    def load(self, source: str) -> list[Document]:
        raise NotImplementedError

@dataclass
class Document:
    content: str
    metadata: dict #来源