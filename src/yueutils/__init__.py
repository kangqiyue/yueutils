"""
yueutils - Common utility functions for Python projects
"""

__version__ = "0.2.0"

from loguru import logger

# Import from data submodules
from .data.utils_json import (
    read_json,
    write_json,
    read_jsonl_data as read_jsonl,
    write_jsonl_data as write_jsonl,
    load_json_or_jsonl,
    write_json_or_jsonl,
)
from .data.utils_polars import (
    read_parquet,
    write_parquet,
    load_json_or_parquet,
    write_json_or_parquet,
)
from .data.cleaner import DataReader

# Import wrapper functions
from .wrapper import time_counter, length_counter, length_counter_before_after

# Import utilities
from .utils import (
    convert_json_to_excel,
    convert_json_to_csv,
    hf_dataset_to_json,
    count_trainable_parameters,
    count_no_trainable_parameters,
    count_parameters,
    get_n_frames,
    generate_filename,
    write_json_clean,
)


def load_data(f_input: str):
    """
    Load data from json, jsonl, or parquet file.

    Args:
        f_input: Input file path

    Returns:
        Loaded data (list or polars DataFrame)

    Raises:
        NotImplementedError: If file extension is not supported
    """
    if f_input.endswith("parquet"):
        return read_parquet(f_input)
    elif f_input.endswith("json"):
        return read_json(f_input)
    elif f_input.endswith("jsonl"):
        return read_jsonl(f_input)
    else:
        raise NotImplementedError(f"ERROR, must be json, jsonl or parquet, but got {f_input}")


def write_data(data: list, f_output: str) -> str:
    """
    Write data to json, jsonl, or parquet file.
    Auto-converts format based on data size for optimal performance.

    Args:
        data: Data to write (list of dicts)
        f_output: Output file path

    Returns:
        Final output file path (may differ if auto-converted)
    """
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

    return f_output


# Export all public APIs
__all__ = [
    # Core functions
    "load_data",
    "write_data",
    # JSON/JSONL functions
    "read_json",
    "write_json",
    "read_jsonl",
    "write_jsonl",
    "load_json_or_jsonl",
    "write_json_or_jsonl",
    # Parquet functions
    "read_parquet",
    "write_parquet",
    "load_json_or_parquet",
    "write_json_or_parquet",
    # Cleaner
    "DataReader",
    # Wrappers
    "time_counter",
    "length_counter",
    "length_counter_before_after",
    # Utilities
    "convert_json_to_excel",
    "convert_json_to_csv",
    "hf_dataset_to_json",
    "count_trainable_parameters",
    "count_no_trainable_parameters",
    "count_parameters",
    "get_n_frames",
    "generate_filename",
    "write_json_clean",
]