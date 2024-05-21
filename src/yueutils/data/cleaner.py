
import json
from functools import wraps
from typing import Callable, List
import jsonlines


def print_len_before_and_after(func: Callable) -> Callable:
    """装饰器函数, 打印输入的数据和输出的数据的length"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 对于类方法，数据可能是第二个参数（在`self`之后）
        # 这里简单地假设数据是第二个参数
        if len(args) > 1:
            data = args[1]
            print(f"Before '{func.__name__}': {len(data)}")
            result = func(*args, **kwargs)  # 调用原始函数
            # 注意处理结果也需要是可测量长度的
            print(f"After '{func.__name__}': {len(result)}")
        else:
            # 如果不是期望的情况（例如没有足够的参数），简单地直接调用函数
            result = func(*args, **kwargs)
        return result
    return wrapper


class DataReader:
    """Read data and write data. support: json, jsonl
    """
    def __init__(self) -> None:
        pass

    def load_data(self, data_file: str) -> list:
        if data_file.endswith(".json"):
            return self.read_json(data_file)
        elif data_file.endswith(".jsonl"):
            return self.read_jsonl_data(data_file)
        else:
            raise NotImplementedError(f"Only support 'json' or 'jsonl', but got {data_file}!")

    def write_data(self, data: list, f_output: str) -> None:
        if f_output.endswith(".json"):
            self.write_json(data=data, f_output=f_output)
        elif f_output.endswith(".jsonl"):
            self.write_jsonl_data(data=data, f_output=f_output)
        else:
            raise NotImplementedError(f"Only support 'json' or 'jsonl', but got {f_output}!")

    @staticmethod
    def read_jsonl_data(data_file):
        data = []
        with open(data_file, 'r', encoding="utf-8") as fd:
            for l in jsonlines.Reader(fd):
                data.append(l)
        print(f"Load:{data_file}\nLen: {len(data)}")
        return data

    @staticmethod
    def write_jsonl_data(data, f_output):
        with jsonlines.open(f_output, 'w') as writer:
            print(f"Saved file in: {f_output}")
            writer.write_all(data)

    @staticmethod
    def read_json(data_file):
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"Load:{data_file}\nLen: {len(data)}")
        return data

    @staticmethod
    def write_json(data, f_output):
        with open(f_output, "w") as f:
            print(f"Save file in: {f_output}")
            json.dump(data, f, ensure_ascii=False, indent=2)


