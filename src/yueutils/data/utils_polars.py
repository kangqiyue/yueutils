import polars as pl
from datasets import Dataset
from ..utils import load_json_or_jsonl, write_json
from ..wrapper import time_counter


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


if __name__ == "__main__":
    flst = [
        "demo.json"
    ]
    data_all = []
    for file in flst:
        data = load_json_or_jsonl(file)
        data_all.extend(data)
    print(len(data_all))

    f_test = f"test_{len(data_all)}.parquet"
    print(f_test)
    save_data_to_pl_parquet(data_all, f_test)
    data = load_data_from_pl_parquet(f_test, return_hf_dataset=False)
