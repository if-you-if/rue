# Python 异步编程指南

## asyncio 基础

asyncio 是 Python 的异步 I/O 库，用于编写并发代码。它基于事件循环（Event Loop）和协程（Coroutine）的概念。

协程使用 `async def` 定义，使用 `await` 调用其他协程：

```python
import asyncio

async def fetch_data(url):
    print(f"开始请求: {url}")
    await asyncio.sleep(1)  # 模拟网络请求
    return {"data": "result"}

async def main():
    result = await fetch_data("https://api.example.com")
    print(result)

asyncio.run(main())
```

## 并发执行多个协程

使用 `asyncio.gather()` 可以并发执行多个协程，所有协程会同时启动，等待全部完成：

```python
async def main():
    results = await asyncio.gather(
        fetch_data("url1"),
        fetch_data("url2"),
        fetch_data("url3"),
    )
    print(results)  # 三个结果同时返回
```

## async/await 与线程的区别

asyncio 是单线程的并发模型，通过协作式多任务实现并发。与多线程相比：

- **优势**：没有 GIL 限制、没有线程切换开销、内存占用更低
- **适用场景**：I/O 密集型任务（网络请求、文件读写、数据库查询）
- **不适用**：CPU 密集型任务（数值计算、图像处理），这类任务应使用 multiprocessing

## 异步上下文管理器

使用 `async with` 语法管理异步资源：

```python
async def read_file(path):
    async with aiofiles.open(path, 'r') as f:
        content = await f.read()
    return content
```

## 异步迭代器

使用 `async for` 遍历异步迭代器：

```python
async def stream_lines(path):
    async with aiofiles.open(path, 'r') as f:
        async for line in f:
            yield line.strip()
```

## 任务取消

可以使用 `Task.cancel()` 取消正在运行的协程：

```python
async def main():
    task = asyncio.create_task(long_running_task())
    await asyncio.sleep(5)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("任务已被取消")
```
