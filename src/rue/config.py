from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_name: str = "qwen2.5:1.5b"
    embedding_model: str = "nomic-embed-text"
    base_url: str = "http://127.0.0.1:11434"
    log_level: str = "info"
    embedding_provider: str = "ollama"  # ollama / onnx
    onnx_model_dir: str = "models/bge-small-zh"
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        
settings = Settings()