

from loguru import logger
from .data.utils_json import read_json, write_json, read_jsonl, write_jsonl
from .data.utils_json import load_json_or_jsonl, write_json_or_jsonl
from .data.utils_polars import read_parquet, write_parquet, load_json_or_parquet, write_json_or_parquet


def load_data(f_input):
    if f_input.endswith("parquet"):
        return read_parquet(f_input)
    elif f_input.endswith("json"):
        return read_json(f_input)
    elif f_input.endswith("jsonl"):
        return read_jsonl(f_input)
    else:
        raise NotImplementedError(f"ERROR, must be json,  josnl or parquet, but got {f_input}")


def write_data(data: list, f_output: str):
    if len(data) >= 20000 and ".json" in f_output:
        f_output = f_output.replace(".json", ".parquet")
        logger.warning(f"change json to parquet for {len(data)} samples | f_output set to: {f_output}")
    elif len(data) >= 20000 and ".jsonl" in f_output:
        f_output = f_output.replace(".jsonl", ".parquet")
        logger.warning(f"change jsonl to parquet for {len(data)} samples | f_output set to: {f_output}")
    elif len(data) < 20000 and ".parquet" in f_output:
        f_output = f_output.replace(".parquet", ".json")
        logger.warning(f"change parquet to json for {len(data)} samples | f_output set to: {f_output}")
        
    if f_output.endswith(".json"):
        write_json(data, f_output)
    elif f_output.endswith(".jsonl"):
        write_jsonl(data, f_output)
    elif f_output.endswith(".parquet"):
        write_parquet(data, f_output)
    else:
        raise NotImplementedError(f"only support json, jsonl or parquet, but got: {f_output}")
   