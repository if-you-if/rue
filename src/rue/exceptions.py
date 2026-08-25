class RueError(Exception):
    """项目中所有自定义异常的基类。"""
    pass


class ConfigurationError(RueError):
    """配置相关的错误，如缺少环境变量。"""
    pass


class ResourceNotFoundError(RueError):
    """资源未找到的错误，如文件不存在。"""
    pass

class ProcessingError(RueError):
    """数据处理过程中发生的错误。"""
    pass