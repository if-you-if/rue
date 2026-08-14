# rue

> 从零构建一个 AI Engineering 项目，逐步实现 LLM、Prompt、Conversation、RAG、MCP 等核心能力。

`rue` 是一个用于学习 AI Engineering 的个人实践项目。

项目不以“调用一个大模型 API”作为最终目标，而是通过逐步实现一个真实的 AI 应用，让自己理解：

- LLM 应用的基本架构
- Prompt Engineering
- Message / ChatRequest / ChatResponse
- LLM 抽象层
- Conversation / Memory
- Context Management
- RAG
- MCP
- Agent
- 本地模型部署

项目坚持一个原则：

> **优先理解原理和架构，再使用成熟框架。**

---

## 1. 当前进度

| Day | 内容 | 状态 |
|---|---|---|
| Day1 | 项目骨架 | ✅ |
| Day2 | 工程结构 / uv 依赖管理 | ✅ |
| Day3 | pydantic-settings 配置系统 | ✅ |
| Day4 | LLM 抽象层 | ✅ |
| Day5 | PromptTemplate | ✅ |
| Day6 | Pydantic Message / ChatRequest / ChatResponse | ✅ |
| Day7 | 接入 Ollama API，实现真实 LLM 调用 | ✅ |
| Day8 | Conversation / 多轮对话 Memory | ✅ |
| Day9 | Context Management | ⏳ |
| Day10+ | 后续规划 | ⏳ |

---
# 2.项目结构(迭代中)
                         rue
                          │
          ┌───────────────┼────────────────┐
          │               │                │
       Models          Prompt           Memory
          │               │                │
          │               │          Conversation
          │               │                │
          ├──── Message   │             Message[]
          ├──── Request   │                │
          └──── Response  │                │
                          │                │
                          ▼                ▼
                     PromptTemplate   Context History
                          │                │
                          └───────┬────────┘
                                  ▼
                               BaseLLM
                                  │
                                  ▼
                             OllamaLLM
                                  │
                                  ▼
                               Ollama
                                  │
                                  ▼
                           qwen2.5:1.5b

# 3. 整体规划
                    rue
                     │
        ┌────────────┼────────────┐
        │            │            │
       LLM          RAG          MCP
        │            │            │
        │            │            │
     Memory       Vector DB     Tools
        │            │            │
        └────────────┼────────────┘
                     │
                   Agent
                     │
                     ▼
              AI Application
# 4. 项目环境

## Python

项目使用 Python 3.12。

## 包管理

使用 `uv` 管理 Python 环境和依赖。

运行项目：

```bash
uv run rue