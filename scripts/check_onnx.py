# check_onnx.py
import onnxruntime as ort

session = ort.InferenceSession(
    "models/bge-small-zh/model.onnx",
    providers=["CPUExecutionProvider"],
)

print("=== 输入 ===")
for inp in session.get_inputs():
    print(f" {inp.name}: shape={inp.shape}, dtype={inp.type}")

print("\n=== 输出 ===")
for out in session.get_outputs():
    print(f" {out.name}: shape={out.shape}, dtype={out.type}")