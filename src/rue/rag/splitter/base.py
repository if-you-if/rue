from abc import ABC, abstractmethod
from dataclasses import dataclass
from rue.rag.loader.base import Document
from .base import Chunk


class TextSplitter(ABC):
   
   @abstractmethod
   def split(self, documents: list[Document]) -> list[Chunk]:
        raise NotImplementedError

@dataclass
class Chunk:
    content: str
    metadata: dict


