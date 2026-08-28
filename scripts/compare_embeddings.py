import time
import numpy as np

from rue.rag.embedding.onnx import OnnxEmbedding
from rue.rag.embedding.ollama import OllamaEmbedding

# ---------- 测试数据 ----------
TEST_TEXTS = [
    # ========== 天气组 ==========
    "今天天气真好，阳光明媚",
    "明天可能会下雨，记得带伞",
    "气温下降了，注意保暖",
    "天气预报说明天有台风，注意安全",
    "秋天的气候最舒适，不冷也不热",
    "夏天的雷阵雨来得快去得也快",

    # ========== 编程组 ==========
    "Python 是一门很流行的编程语言",
    "机器学习需要大量的数据训练",
    "Git 是常用的版本控制工具",
    "Docker 让应用部署变得更加简单",
    "前端开发离不开 JavaScript",
    "数据库优化是后端开发的核心技能",

    # ========== 美食组 ==========
    "这家餐厅的红烧肉做得非常好吃",
    "我喜欢吃水果，尤其是苹果和香蕉",
    "早餐喝一杯牛奶很有营养",
    "火锅是冬天最受欢迎的美食",
    "广式早茶的虾饺晶莹剔透",
    "自己做饭比外卖更健康",

    # ========== 运动组 ==========
    "跑步是最简单有效的有氧运动",
    "打篮球可以锻炼身体协调性",
    "瑜伽有助于放松身心",
    "游泳是一项全身运动",
    "每天坚持散步对心血管健康有益",
    "力量训练可以增强肌肉和骨骼",

    # ========== 学习组 ==========
    "读书可以增长见识，开阔眼界",
    "学一门外语能打开新的世界",
    "在线课程让学习变得更加便捷",
    "做笔记是提高学习效率的好方法",

    # ========== 科技组 ==========
    "人工智能正在改变我们的生活方式",
    "5G 技术将推动物联网的发展",
    "区块链在金融领域有广泛应用",
    "自动驾驶汽车正在逐步普及",

    # ========== 生活组 ==========
    "旅行是认识世界的好方式",
    "早睡早起对身体有很多好处",
    "听音乐可以缓解压力和焦虑",
    "养宠物能给人带来陪伴和快乐",

    # ========== 职场组 ==========
    "团队合作是项目成功的关键",
    "时间管理能力决定工作效率",
    "职场沟通需要学会倾听和表达",
    "持续学习是职业发展的基石",
]

QUERIES = [
    # 天气类
    "今天下雨了吗",
    "明天天气怎么样",
    "冬天冷不冷",
    
    # 编程类
    "怎么学编程",
    "Git 怎么用",
    
    # 美食类
    "推荐一道好吃的菜",
    "早餐吃什么有营养",
    
    # 运动类
    "什么运动最适合减肥",
    "怎么锻炼身体",
    
    # 跨类别
    "如何提高生活质量",
    "科技进步带来了什么",
]

def measure_speed(embedding, texts, label):
    start = time.perf_counter()
    vectors = embedding.embed_batch(texts)
    elapsed = time.perf_counter() - start
    print(f"\n{label}:")
    print(f" 总耗时: {elapsed:.3f}s")
    print(f" 单条平均 {elapsed / len(texts) * 1000: .1f}ms")
    return elapsed, vectors

def cosine_similarity(v1, v2):
    a = np.array(v1)
    b = np.array(v2)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def compare_ranking(ollama_emb, onnx_emb, texts, query):
    # 单独对 query 做 embedding
    q_ollama = ollama_emb.embed(query)
    q_onnx = onnx_emb.embed(query)

    # 对所有文本做 embedding
    vecs_ollama = ollama_emb.embed_batch(texts)
    vecs_onnx = onnx_emb.embed_batch(texts)

    # 计算查询和每条文本的相似度
    scores_ollama = [(text, cosine_similarity(q_ollama, v)) for text, v in zip(texts, vecs_ollama)]
    scores_onnx = [(text, cosine_similarity(q_onnx, v)) for text, v in zip(texts, vecs_onnx)]

    # 按相似度降序排序
    scores_ollama.sort(key=lambda x: x[1], reverse=True)
    scores_onnx.sort(key=lambda x: x[1], reverse=True)

    print(f"\n查询句: {query}")
    print(f"\n{'排名':<4} {'Ollama':<40} {'得分':<8} | {'ONNX':<40} {'得分':<8}")
    print("-" * 110)

    for i in range(len(scores_ollama)):
        t_o, s_o = scores_ollama[i]
        t_n, s_n = scores_onnx[i]
        print(f" {i+1:<3} {t_o:<40} {s_o:<8.4f} | {t_n:<40} {s_n:<8.4f}")

    for k in [1, 3, 5]:
        ollama_topk = {t for t, _ in scores_ollama[:k]}
        onnx_topk = {t for t, _ in scores_onnx[:k]}
        overlap = ollama_topk & onnx_topk
        print(f"\nTop-{k} 重合度: {len(overlap)}/{k} = {len(overlap)/k:.0%}")

def main():
    print("=" * 60)
    print("Embedding 对比测试")
    print(f"测试文本数: {len(TEST_TEXTS)}")
    print("=" * 60)

    #初始化
    ollama_emb = OllamaEmbedding()
    onnx_emb = OnnxEmbedding()

    t_ollama, vecs_ollama = measure_speed(ollama_emb, TEST_TEXTS, "OllamaEmbedding")
    t_onnx, vecs_onnx = measure_speed(onnx_emb, TEST_TEXTS, "OnnxEmbedding")

    speedup = t_ollama / t_onnx if t_onnx > 0 else 0
    print(f"\n速度对比: ONNX 是 Ollama 的{speedup:.1f} 倍")

    for query in QUERIES:
        compare_ranking(ollama_emb, onnx_emb, TEST_TEXTS, query)


if __name__ == "__main__":
    main()


