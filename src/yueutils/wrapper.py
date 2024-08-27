


import time
from functools import wraps
from typing import Callable, List


# time wraper
def time_counter(func):
    """time counter"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' took {end_time - start_time:.6f} seconds to run.")
        return result
    return wrapper


# length wrapper
def length_counter(func: Callable) -> Callable:
    """打印输入的数据和输出的数据的length"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 对于类方法，数据可能是第二个参数（在`self`之后）
        # 这里简单地假设数据是第二个参数
        if len(args) > 1:
            result = func(*args, **kwargs)  # 调用原始函数
            # 注意处理结果也需要是可测量长度的
            print(f"Length After '{func.__name__}': {len(result)}")
        else:
            # 如果不是期望的情况（例如没有足够的参数），简单地直接调用函数
            result = func(*args, **kwargs)
        return result
    return wrapper


def length_counter_before_after(func: Callable) -> Callable:
    """打印输入的数据和输出的数据的length"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 对于类方法，数据可能是第二个参数（在`self`之后）
        # 这里简单地假设数据是第二个参数
        if len(args) > 1 and isinstance(args[1], List):
            data = args[1]
            print(f"Length Before '{func.__name__}': {len(data)}")
            result = func(*args, **kwargs)  # 调用原始函数
            # 注意处理结果也需要是可测量长度的
            print(f"Length After '{func.__name__}': {len(result)}")
        else:
            # 如果不是期望的情况（例如没有足够的参数），简单地直接调用函数
            result = func(*args, **kwargs)
        return result
    return wrapper