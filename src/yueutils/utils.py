import toml
import jsonlines
import os
import time
import json
import pandas as pd
from datetime import datetime



'''calculate time'''
def time_counter(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' took {end_time - start_time:.6f} seconds to run.")
        return result
    return wrapper



'''jsonlines utils'''
def read_jsonl_data(f_input):
    data = []
    with open(f_input, 'r', encoding="utf-8") as fd:
        for l in jsonlines.Reader(fd):
            data.append(l)
    return data

def write_jsonl_data(res, f_output):
    with jsonlines.open(f_output, 'w') as writer:
        writer.write_all(res)

def read_json(f_input):
    with open(f_input, "r") as f:
        data = json.load(f)
    print(f"len of {f_input}:\n {len(data)}")
    return data

def write_json(res, f_output):
    with open(f_output, "w") as f:
        print(f_output)
        json.dump(res, f, ensure_ascii=False, indent=2)


def load_json_or_jsonl(f_input):
    if f_input.endswith("jsonl"):
        return read_jsonl_data(f_input)
    elif f_input.endswith("json"):
        return read_json(f_input)
    else:
        raise NotImplementedError(f"ERROR, must be json or jsonl, but got {f_input}")


"""convert josn to csv or excel"""
def convert_json_to_excel(file_name):
    data = read_json(file_name)
    df = pd.DataFrame(data)
    f_outupt = file_name.replace(".json", ".xlsx")
    df.to_excel(f_outupt)
    print(f"save file as: {f_outupt}")

def convert_json_to_csv(file_name):
    """
    convert json to csv
    Args:
        file_name:

    Returns:
        None
    """
    data = read_json(file_name)
    df = pd.DataFrame(data)
    f_outupt = file_name.replace(".json", ".csv")
    df.to_csv(f_outupt)
    print(f"save file as: {f_outupt}")


def hg_dataset_to_json(dataset):
    """
    convert huggingface dataset to json
    Args:
        dataset: Huggingface dataset

    Returns:
        data: list of dict
    """
    import pandas as pd
    df = pd.DataFrame(dataset)
    return df.to_dict(orient="records")



'''count model parameters'''
def count_trainable_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

def count_no_trainable_parameters(model):
    return sum(p.numel() for p in model.parameters() if not p.requires_grad)

def count_parameters(model):
    return sum(p.numel() for p in model.parameters())


'''get n frame from a video'''
def get_n_frames(start, end, n):
    """
    start: 取整数的起点
    end: 取整数的终点
    n: 取的整数数量
    """
    step = int((end - start) / (n - 1)) # 计算步长
    return [start + step * i for i in range(n)] # 返回等间隔的n个整数


"""generate file name"""
def generate_filename(data_source, from_model, date=None, data=None, comment=None, is_raw=False, additional_info=None, extension="json"):
    """
    生成遵循规定命名规则的文件名。

    :param date: 文件的日期，格式为 'YYYYMMDD' 或 datetime 对象。
    :param data_source: data prompt来源
    :param model: 生成数据的模型
    :param additional_info: （可选）文件的附加信息。
    :param extension: （默认为 'json'）文件扩展名。
    :param comment: （可选）关于文件的注释。
    :return: 根据参数构造的文件名字符串。
    """
    if date is None:
        date = datetime.now()

    # 如果日期是 datetime 对象，则转换为字符串
    if isinstance(date, datetime):
        date_str = date.strftime("%Y%m%d")
    else:
        date_str = date

    # 构建基本的文件名
    from_model = f"from-{from_model}"
    filename_elements = [date_str, data_source, from_model]
    if additional_info:
        filename_elements.append(additional_info)
    if is_raw:
        filename_elements.append("raw")

    # 添加注释到文件名（如果有）
    if comment:
        # 确保注释中不包含非法文件名字符
        safe_comment = "".join([c for c in comment if c.isalnum() or c in ("_", "-")])
        # safe_comment = safe_comment.replace("_", "-")
        filename_elements.append(f"comment-{safe_comment}")

    filename_elements = [i.replace("_", "-") for i in filename_elements]
    if data:
        filename = "_".join(filename_elements) + f"_{str(len(data))}.{extension}"
    else:
        filename = "_".join(filename_elements) + f".{extension}"

    return filename


def write_json_clean(data, f_save_path, f_save_name):
    f_output = os.path.join(f_save_path, f_save_name)
    write_json(data, f_output=f_output)


if __name__ == "__mian__":
    pass
