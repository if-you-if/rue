from rue.rag.document import Document
from dataclasses import dataclass


@dataclass
class Chunk:
    content: str
    metadata: dict #来源