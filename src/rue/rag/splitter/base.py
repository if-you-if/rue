from abc import ABC, abstractmethod
from rue.rag.document import Document
from rue.rag.chunk import Chunk


class TextSplitter(ABC):
   
   @abstractmethod
   def split(self, documents: list[Document]) -> list[Chunk]:
        raise NotImplementedError


