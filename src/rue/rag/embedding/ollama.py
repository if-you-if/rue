from rue.rag.embedding.base import BaseEmbedding
from rue.config import settings
import httpx

class OllamaEmbedding(BaseEmbedding):

    def __init__(self, model: str | None = None):
        self.model = model or settings.model_name
        self.endpoint = f"{settings.base_url.rstrip('/')}/api/embeddings"
    
    def embed(self, text: str) -> list[float]:
        
        payload = {
            "model": self.model,
            "prompt": text,
        }

        with httpx.Client() as client:
            res = client.post(self.endpoint, json=payload, timeout=60.0)
            res.raise_for_status()
            return res.json()["embedding"]