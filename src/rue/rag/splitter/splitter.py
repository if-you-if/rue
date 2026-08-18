from rue.rag.splitter.base import TextSplitter
from rue.rag.loader.base import Document
from rue.rag.splitter.base import Chunk


class RecursiveCharacterSplitter(TextSplitter):
    def __init__(self, chunk_size: int, chunk_overlap: int):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, documents: list[Document]) -> list[Chunk]:
        raise NotImplementedError