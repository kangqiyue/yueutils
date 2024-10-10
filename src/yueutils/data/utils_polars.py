import polars as pl
from datasets import Dataset
from ..utils import load_json_or_jsonl, write_json, read_json
from ..wrapper import time_counter
from loguru import logger


@time_counter
def load_data_from_pl_parquet(f_input, return_hf_dataset=False):
    assert f_input.endswith("parquet")
    # # slow 
    # data = pl.read_parquet(f_input)
    # data = data.to_pandas()
    # data = Dataset.from_pandas(data)
    # fast
    data = pl.read_parquet(f_input)
    if return_hf_dataset:
        data = Dataset.from_polars(data)
    return data


@time_counter
def save_data_to_pl_parquet(data: list, f_output: str, demo_num: int = 20):
    """
    data: list of dict
    f_output: output name
    """
    # save demo
    if demo_num is not None:
        demo_data = data[0:demo_num]
        f_demo_output = f_output.replace(".parquet", "_demo.json")
        write_json(demo_data, f_demo_output)
    
    # save data
    df =  pl.DataFrame(data)
    df.write_parquet(f_output)
    print(f"save {len(df)} samples in: {f_output}")

# alias function 
# load -- save
read_parquet = load_data_from_pl_parquet
write_parquet = save_data_to_pl_parquet
# read -- write
load_parquet = load_data_from_pl_parquet
save_parquet = save_data_to_pl_parquet


def load_json_or_parquet(f_input):
    if f_input.endswith("parquet"):
        return read_parquet(f_input)
    elif f_input.endswith("json"):
        return read_json(f_input)
    else:
        raise NotImplementedError(f"ERROR, must be json or parquet, but got {f_input}")


def write_json_or_parquet(data: list, f_output: str):
    if len(data) >= 20000 and ".json" in f_output:
        f_output = f_output.replace(".json", ".parquet")
        logger.warning(f"change json to parquet for {len(data)} samples | f_output set to: {f_output}")
    elif len(data) < 20000 and ".parquet" in f_output:
        f_output = f_output.replace(".parquet", ".json")
        logger.warning(f"change parquet to json for {len(data)} samples | f_output set to: {f_output}")
    if f_output.endswith(".json"):
        write_json(data, f_output)
    elif f_output.endswith(".parquet"):
        save_data_to_pl_parquet(data, f_output)
    else:
        raise NotImplementedError(f"only support json or parquet, but got: {f_output}")
   

if __name__ == "__main__":
    pass