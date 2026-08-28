from pydantic_settings import BaseSettings
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    model_name: str = "qwen2.5:1.5b"
    embedding_model: str = "nomic-embed-text"
    base_url: str = "http://127.0.0.1:11434"
    log_level: str = "info"
    embedding_provider: str = "ollama"  # ollama / onnx
    
    onnx_model_dir: str = "src/rue/models/bge-small-zh"  
    vector_db_path: str = "data/vector_db"   
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        
settings = Settings()