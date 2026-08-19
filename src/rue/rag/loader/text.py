from pathlib import Path
from rue.rag.loader.base import BaseLoader
from rue.rag.document import Document

class TextLoader(BaseLoader):

    def __init__(self, encoding: str = "utf-8"):
        self.encoding = encoding
    
    def load(self, source: str) -> list[Document]:
        path = Path(source)
        content = path.read_text(encoding=self.encoding)
        return [Document(
            content=content,
            metadata={"source": str(path), "type": path.suffix}
        )]