import toml
import jsonlines
import os
import time
import json
import pandas as pd


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


'''path utils'''
def mkdir(input_path):
    if not os.path.exists(input_path):
        os.makedirs(input_path)
    else:
        print(f"the path esxits: {input_path}")


def list_files(endwith=None):
    if endwith is not None:
        files = []
        for file in os.listdir('..'):
            if file.endswith('.png'):
                files.append(file)
        return files
    else:
        files = []
        for file in os.listdir('..'):
            files.append(file)
        return files

def list_files_all(input_path):
    lst = []
    for path, subdirs, files in os.walk(input_path):
        for name in files:
            # print(os.path.join(path, name))
            lst.append(os.path.join(path, name))
    return lst


'''jsonlines utils'''
def read_jsonl_data(path_and_name):
    data = []
    with open(path_and_name, 'r', encoding="utf-8") as fd:
        for l in jsonlines.Reader(fd):
            data.append(l)
    return data

def write_jsonl_data(items, path_and_name):
    with jsonlines.open(path_and_name, 'w') as writer:
        writer.write_all(items)

def read_jsonl_lst(lst_file):
    '''
    :param lst_file: list of jsonl file
    :return: merged jsonl list data
    '''
    datas = []
    for i in lst_file:
        with open(i ,'r',encoding="utf-8") as fd:
            for l in jsonlines.Reader(fd):
                datas.append(l)
    return datas

def read_txt_data(path_and_name):
    with open(path_and_name) as f:
        lines = f.readlines()
    return lines

def read_json(file):
    with open(file, "r") as f:
        data = json.load(f)
    print(f"len of {file}:\n {len(data)}")
    return data

def write_json(result, f_output):
    with open(f_output, "w") as f:
        print(f_output)
        json.dump(result, f, ensure_ascii=False, indent=2)


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


if __name__ == "__mian__":
    pass