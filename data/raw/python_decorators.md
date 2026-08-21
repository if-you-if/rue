# Python 装饰器详解

## 什么是装饰器

装饰器是 Python 中一种强大的语法糖，本质上是一个接受函数作为参数并返回新函数的可调用对象。装饰器允许你在不修改原函数代码的情况下，动态地为函数添加额外功能。

## 基本语法

使用 `@decorator_name` 语法将装饰器应用到函数上：

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("函数执行前")
        result = func(*args, **kwargs)
        print("函数执行后")
        return result
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")
```

## 带参数的装饰器

装饰器本身也可以接受参数，这需要三层嵌套：

```python
def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"Hello, {name}!")
```

## 常用内置装饰器

Python 提供了几个常用的内置装饰器：

- `@staticmethod`：将方法定义为静态方法，不需要 self 参数
- `@classmethod`：将方法定义为类方法，第一个参数是 cls
- `@property`：将方法定义为属性，可以像属性一样访问
- `@functools.wraps`：保留原函数的元数据（名称、文档字符串等）

## 类装饰器

除了函数装饰器，Python 还支持类装饰器。类装饰器通过 `__call__` 方法实现：

```python
class Counter:
    def __init__(self, func):
        self.func = func
        self.count = 0
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"{self.func.__name__} 已被调用 {self.count} 次")
        return self.func(*args, **kwargs)
```

## 装饰器的执行顺序

当多个装饰器叠加使用时，装饰器的执行顺序是从下到上（靠近函数的先执行），但调用顺序是从上到下：

```python
@decorator_a
@decorator_b
def my_func():
    pass

# 等价于：my_func = decorator_a(decorator_b(my_func))
```
