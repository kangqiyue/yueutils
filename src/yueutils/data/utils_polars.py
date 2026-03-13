import polars as pl
from pathlib import Path
from typing import List, Dict, Any, Union, Optional
from datasets import Dataset
from loguru import logger

from ..wrapper import time_counter


@time_counter
def load_data_from_pl_parquet(
    f_input: str,
    return_hf_dataset: bool = False
) -> Union[pl.DataFrame, Dataset]:
    """Load data from Parquet file using Polars.

    Args:
        f_input: Input Parquet file path
        return_hf_dataset: If True, return HuggingFace Dataset instead of DataFrame

    Returns:
        Polars DataFrame or HuggingFace Dataset
    """
    suffix = Path(f_input).suffix.lower()
    assert suffix == ".parquet", f"Expected .parquet file, got {f_input}"

    data = pl.read_parquet(f_input)
    logger.info(f"Loaded {len(data)} records from {f_input}")

    if return_hf_dataset:
        data = Dataset.from_polars(data)

    return data


@time_counter
def save_data_to_pl_parquet(
    data: List[Dict[str, Any]],
    f_output: str,
    demo_num: Optional[int] = 20
) -> None:
    """Save data to Parquet file using Polars.

    Args:
        data: List of dictionaries to save
        f_output: Output Parquet file path
        demo_num: Number of samples to save as demo JSON file. None to skip demo.
    """
    # Save demo file for quick inspection
    if demo_num is not None and demo_num > 0:
        from .utils_json import write_json
        demo_data = data[:demo_num]
        output_path = Path(f_output)
        f_demo_output = str(output_path.with_stem(f"{output_path.stem}_demo").with_suffix(".json"))
        write_json(demo_data, f_demo_output)

    # Save full data as Parquet
    df = pl.DataFrame(data)
    df.write_parquet(f_output)
    logger.info(f"Saved {len(df)} records to {f_output}")

# Aliases for backward compatibility
read_parquet = load_data_from_pl_parquet
write_parquet = save_data_to_pl_parquet
load_parquet = load_data_from_pl_parquet
save_parquet = save_data_to_pl_parquet


def load_json_or_parquet(f_input: str) -> Union[List[Dict[str, Any]], pl.DataFrame]:
    """Load data from JSON or Parquet file.

    Args:
        f_input: Input file path (.json or .parquet)

    Returns:
        List of dicts (for JSON) or Polars DataFrame (for Parquet)

    Raises:
        NotImplementedError: If file extension is not .json or .parquet
    """
    from .utils_json import read_json

    suffix = Path(f_input).suffix.lower()

    if suffix == ".parquet":
        return read_parquet(f_input)
    elif suffix == ".json":
        return read_json(f_input)
    else:
        raise NotImplementedError(f"ERROR, must be .json or .parquet, but got {f_input}")


def write_json_or_parquet(data: List[Dict[str, Any]], f_output: str) -> str:
    """Write data to JSON or Parquet file with automatic format optimization.

    Automatically converts to Parquet for large datasets (>=20k records).

    Args:
        data: List of dictionaries to write
        f_output: Output file path (.json or .parquet)

    Returns:
        Final output file path (may differ if auto-converted)

    Raises:
        NotImplementedError: If file extension is not .json or .parquet
    """
    from .utils_json import write_json

    output_path = Path(f_output)
    suffix = output_path.suffix.lower()

    # Auto-optimize format based on data size
    if len(data) >= 20000 and suffix == ".json":
        output_path = output_path.with_suffix(".parquet")
        f_output = str(output_path)
        logger.warning(
            f"Auto-converting to Parquet for {len(data)} records | "
            f"Output: {f_output}"
        )
    elif len(data) < 20000 and suffix == ".parquet":
        output_path = output_path.with_suffix(".json")
        f_output = str(output_path)
        logger.warning(
            f"Auto-converting to JSON for {len(data)} records | "
            f"Output: {f_output}"
        )

    # Write based on final suffix
    suffix = output_path.suffix.lower()
    if suffix == ".json":
        write_json(data, f_output)
    elif suffix == ".parquet":
        save_data_to_pl_parquet(data, f_output)
    else:
        raise NotImplementedError(f"Only support .json or .parquet, but got: {f_output}")

    return f_output
   

if __name__ == "__main__":
    pass