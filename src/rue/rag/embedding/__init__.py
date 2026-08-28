from chromadb.execution.expression.operator import Val
from rue.config import settings
from rue.rag.embedding.base import BaseEmbedding
from rue.rag.embedding.ollama import OllamaEmbedding
from rue.rag.embedding.onnx import OnnxEmbedding


def get_embedding() -> BaseEmbedding:

    provider = settings.embedding_provider.lower()
    if provider == "onnx":
        return OnnxEmbedding()
    elif provider == "ollama":
        return OllamaEmbedding()
    else:
        raise ValueError(f"不支持的 embedding provider: {provider}")


__all__ = ["BaseEmbedding", "OllamaEmbedding", "OnnxEmbedding", "get_embedding"]