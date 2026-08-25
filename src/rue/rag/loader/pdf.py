
from rue.rag.loader.base import BaseLoader
import fitz
from pathlib import Path
from rue.rag.document import Document
from rue.exceptions import ResourceNotFoundError
from rue.rag.exceptions import PDFLoaderError,ProcessingError

class PDFLoader(BaseLoader):

    def __init__(self) -> None:
        super().__init__()

    def load(self, source: str) -> list[Document]:
        file_path = Path(source)

        if not file_path.exists():
            raise ResourceNotFoundError(f"PDF文件不存在: {source}")
        if file_path.suffix.lower() != '.pdf':
            raise PDFLoaderError(f"不支持的文件格式: {file_path.suffix}")

        docs = []
        try:
            with fitz.open(source) as doc:
                
                for page_num in range(len(doc)):
                    page = doc[page_num]
                    text = page.get_text()

                    metadata = {
                        "source": source,
                        "page_num": page_num + 1,
                        "total_pages": len(doc),
                    }

                    docs.append(Document(content=text, metadata=metadata))

            return docs

        except fitz.fitz.FitzError as e:
            raise ProcessingError(f"PDF解析失败: {source}") from e
        except Exception as e:
            raise PDFLoaderError(f"加载PDF失败: {source}") from e


