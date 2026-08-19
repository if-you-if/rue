import chunk
from rue.rag.splitter.base import TextSplitter
from rue.rag.document import Document
from rue.rag.chunk import Chunk


class RecursiveCharacterSplitter(TextSplitter):
    """按分隔符优先级递归分割文本
    
    分隔符优先级: 段落(\n) -> 句子(.!?)->空格->字符
    """

    def __init__(
        self, 
        chunk_size: int, 
        chunk_overlap: int,
        separators: list[str] | None = None
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", "。", ".", "!", "！", "?", "？", " ", ""]
        

    def split(self, documents: list[Document]) -> list[Chunk]:
        chunks = []
        for doc in documents:
            text_chunks = self._split_text(doc.content)
            for text in text_chunks:
                chunks.append(Chunk(content=text, metadata=doc.metadata.copy()))
        return chunks
    
    def _split_text(self, text: str) -> list[str]:
        return self._recursive_split(text, self.separators)
    
    def _recursive_split(self, text: str, separators: list[str]) -> list[str]:
        if len(text) <= self.chunk_size:
            return [text] if text.strip() else []

        separator = separators[0] if separators else ""
        remaining_separators = separators[1:] if len(separators) > 1 else []

        if separator == "":
            
            parts = list(text)
        else:
            parts = text.split(separator)
        
        chunks = []
        current = ""

        for part in parts:
            candidate = current + separator + part if current else part
            if len(candidate) <= self.chunk_size:
                current = candidate
            else:
                if current:
                    chunks.append(current)
                if len(part) > self.chunk_size and remaining_separators:
                    chunks.extend(self._recursive_split(part, remaining_separators))
                else:
                    current = part
                    continue
                current = ""

        if current:
            chunks.append(current)
        
        if self.chunk_overlap > 0 and len(chunks) > 1:
            chunks = self._add_overlap(chunks)
        return chunks
    
    def _add_overlap(self, chunks: list[str]) -> list[str]:

        result = [chunks[0]]
        for i in range(1, len(chunks)):
            overlap_text = chunks[i-1][-self.chunk_overlap:]
            result.append(overlap_text + chunks[i])
        
        return result

                

