from tokenizers import Tokenizer
from typing import Optional, Callable
from rue.config import settings
from rue.rag.embedding.base import BaseEmbedding
from pathlib import Path
import onnxruntime as ort
import numpy as np

class OnnxEmbedding(BaseEmbedding):
    
    def __init__(
        self,
        model_dir: Optional[str] = Path(model_dir) if model_dir else Path(settings.onnx_model_dir),
        max_length: int = 512,
        normalize: bool = True,
        pooling: str = "cls"
    ):
        self.model_dir = Path(model_dir) if model_dir else _default_model_dir()
        self.max_length = max_length
        self.normalize = normalize
        self._pooling = pooling

        if model_dir is None or not model_dir.strip():
            self.model_dir = _default_model_dir()
        else:
            self.model_dir = Path(model_dir)

        if self._pooling not in ["cls", "mean"]:
            raise ValueError(f"pooling 只支持 'cls' 或 'mean', 当前为: {self._pooling}")

        # 加载 tokenizer
        tokenizer_path = self.model_dir / "tokenizer.json"
        if not tokenizer_path.exists():
            raise FileNotFoundError(f"tokenizer.json 不存在: {tokenizer_path}")
        self._tokenizer = Tokenizer.from_file(str(tokenizer_path))
        self._tokenizer.enable_truncation(max_length=max_length)
        self._tokenizer.enable_padding(length=max_length)

        # 加载 ONNX 模型
        model_path = self.model_dir / "model.onnx"
        if not model_path.exists():
            raise FileNotFoundError(f"model.onnx 不存在: {model_path}")
        self._session = ort.InferenceSession(
            str(model_path),
            providers=["CPUExecutionProvider"],
        )
        self._input_names = [inp.name for inp in self._session.get_inputs()]
        self._embedding_dim = self._session.get_outputs()[0].shape[-1]

    def embed(self, text: str) -> list[float]:
        return self.embed_batch([text])[0]

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """入口：处理空文本，保证输出数量与输入一致"""
        if not texts:
            return []

        # 1. 标记空文本
        is_empty = [not t or not t.strip() for t in texts]

        # 2. 提取非空文本
        nonempty_texts = [t for t in texts if t and t.strip()]

        # 3. 如果全部为空，直接返回零向量
        if not nonempty_texts:
            return [[0.0] * self._embedding_dim for _ in texts]

        # 4. 对非空文本做 embedding
        embeddings = self._embed_nonempty(nonempty_texts)

        # 5. 恢复原始顺序，空位置填零向量
        return self._restore_order(embeddings, is_empty)

    # ---------- 内部核心方法 ----------
    def _embed_nonempty(self, texts: list[str]) -> list[list[float]]:
        """假设 texts 全部非空，执行完整 embedding 流程"""
        # 调用纯推理方法
        embeddings_np = self._inference(texts)
        # 归一化（如果需要）
        if self.normalize:
            norms = np.linalg.norm(embeddings_np, axis=1, keepdims=True)
            norms = np.maximum(norms, 1e-12)
            embeddings_np = embeddings_np / norms
        return embeddings_np.tolist()

    def _inference(self, texts: list[str]) -> np.ndarray:
        """纯 ONNX 推理，返回未归一化的 embeddings (numpy)"""
        # Tokenize
        encodings = self._tokenizer.encode_batch(texts)
        input_ids = [e.ids for e in encodings]
        attention_mask = [e.attention_mask for e in encodings]
        token_type_ids = [e.type_ids for e in encodings]

        # 构建 feed
        feed = {}
        if "input_ids" in self._input_names:
            feed["input_ids"] = np.array(input_ids, dtype=np.int64)
        if "attention_mask" in self._input_names:
            feed["attention_mask"] = np.array(attention_mask, dtype=np.int64)
        if "token_type_ids" in self._input_names:
            feed["token_type_ids"] = np.array(token_type_ids, dtype=np.int64)

        # 推理
        outputs = self._session.run(None, feed)
        last_hidden_state = outputs[0]  # (batch, seq_len, hidden)

        # Pooling（策略模式）
        pool_func = self._get_pooling_func()
        attention_mask_np = np.array(attention_mask, dtype=np.float32)
        return pool_func(last_hidden_state, attention_mask_np)

    def _restore_order(self, embeddings: list[list[float]], is_empty: list[bool]) -> list[list[float]]:
        """根据空标记恢复顺序，空位置填零向量"""
        result = []
        empty_idx = 0
        dim = len(embeddings[0]) if embeddings else self._embedding_dim
        for flag in is_empty:
            if flag:
                result.append([0.0] * dim)
            else:
                result.append(embeddings[empty_idx])
                empty_idx += 1
        return result

    # ---------- Pooling 策略 ----------
    def _pool_cls(self, last_hidden_state: np.ndarray, attention_mask: np.ndarray) -> np.ndarray:
        return last_hidden_state[:, 0, :]

    def _pool_mean(self, last_hidden_state: np.ndarray, attention_mask: np.ndarray) -> np.ndarray:
        raise NotImplementedError("Mean pooling 暂未实现")

    def _get_pooling_func(self) -> Callable:
        pool_funcs = {
            "cls": self._pool_cls,
            "mean": self._pool_mean,
        }
       
        return pool_funcs[self._pooling]


def _default_model_dir() -> Path:
    project_root = Path(__file__).resolve().parents[4]
    return project_root / "models" / "bge-small-zh"