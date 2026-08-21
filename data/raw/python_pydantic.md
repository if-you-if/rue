# Pydantic 数据验证框架

## Pydantic 简介

Pydantic 是 Python 最流行的数据验证库，利用类型注解（Type Hints）实现数据验证、序列化和转换。它比手动编写验证代码更简洁、更可靠。

## 基本模型定义

使用 `BaseModel` 创建数据模型，字段类型会自动验证：

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str
    age: int = Field(ge=0, le=150, description="年龄必须在0-150之间")
    email: str
    
    class Config:
        str_strip_whitespace = True
```

## 数据验证

Pydantic 会自动进行类型转换和验证：

```python
# 自动类型转换
user = User(name="张三", age="25", email="zhangsan@example.com")
# age 从字符串 "25" 自动转换为整数 25

# 验证失败会抛出 ValidationError
try:
    user = User(name="李四", age=-1, email="invalid")
except ValidationError as e:
    print(e)
```

## Field 高级用法

`Field` 提供了丰富的验证和元数据选项：

```python
class Product(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0, description="价格必须大于0")
    tags: list[str] = Field(default_factory=list)
    discount: float = Field(default=0.0, ge=0, le=1)
```

## 嵌套模型

Pydantic 支持模型嵌套，子模型会自动验证：

```python
class Address(BaseModel):
    city: str
    street: str

class Employee(BaseModel):
    name: str
    address: Address  # 嵌套模型
    skills: list[str]
```

## 自定义验证器

使用 `@field_validator` 添加自定义验证逻辑：

```python
from pydantic import BaseModel, field_validator

class Order(BaseModel):
    quantity: int
    price: float
    
    @field_validator("price")
    @classmethod
    def validate_price(cls, v, info):
        if v <= 0:
            raise ValueError("价格必须大于0")
        return round(v, 2)
```

## 序列化

Pydantic 模型可以轻松转换为字典或 JSON：

```python
user = User(name="张三", age=25, email="test@example.com")
data = user.model_dump()          # 转为字典
json_str = user.model_dump_json()  # 转为 JSON 字符串
```

## Pydantic Settings

`pydantic-settings` 扩展支持从环境变量和配置文件加载设置：

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    api_key: str
    debug: bool = False
    
    class Config:
        env_file = ".env"
```
