from rue.exceptions import RueError,ProcessingError

class RAGError(RueError):
    """RAG 模块的基础异常。"""
    pass

class DocumentLoaderError(RAGError, ProcessingError):
    """文档加载器相关的异常基类。"""
    pass

class PDFLoaderError(DocumentLoaderError):
    """PDF 加载器专有异常。"""
    pass

class PDFParsingError(PDFLoaderError):
    """PDF 解析失败（格式错误、加密等）。"""
    pass