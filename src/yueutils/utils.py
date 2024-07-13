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


'''print utils'''
def print_args(*args, **kwargs): #print args
    for arg in args:
        print(f"{arg}")
    for key, value in kwargs.items():
        print("%s == %s" % (key, value))

def print_space(strings): #print with space
    print()
    print(strings)
    print()


'''init config utils'''
def init_config(config_file):
    config_dict=toml.load(config_file, _dict=dict)
    hf_config = config_dict["HFToken"]
    wandb_config = config_dict["WandbToken"]
    return config_dict,hf_config,wandb_config

def init_env_hf_wandb(config_file=None):
    if config_file is not None:
        config_file = config_file
    else:
        config_file = "./configs/configs.toml"
    config_dict, hf_config, wandb_config = init_config(config_file)
    YOUR_TOKEN = hf_config["Val"]
    os.environ["WANDB_API_KEY"] = wandb_config["Val"]
    os.environ["YOUR_TOKEN"] = YOUR_TOKEN
    print(f"init WandbToken and HFToken finished!")
    return


'''jsonlines utils'''
def read_jsonl_data(data_file):
    data = []
    with open(data_file, 'r', encoding="utf-8") as fd:
        for l in jsonlines.Reader(fd):
            data.append(l)
    return data

def write_jsonl_data(items, data_file):
    with jsonlines.open(data_file, 'w') as writer:
        writer.write_all(items)

def read_txt_data(path_and_name):
    with open(path_and_name) as f:
        lines = f.readlines()
    return lines

def read_json(data_file):
    with open(data_file, "r") as f:
        data = json.load(f)
    print(f"len of {data_file}:\n {len(data)}")
    return data

def write_json(result, f_output):
    with open(f_output, "w") as f:
        print(f_output)
        json.dump(result, f, ensure_ascii=False, indent=2)


def load_json_or_jsonl(data_file):
    if data_file.endswith("jsonl"):
        return read_jsonl_data(data_file)
    elif data_file.endswith("json"):
        return read_json(data_file)
    else:
        raise NotImplementedError(f"ERROR, must be json or jsonl, but got {data_file}")


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
