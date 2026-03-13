import os
import csv
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from loguru import logger

from .data.utils_json import (
    read_json, write_json, read_jsonl_data as read_jsonl,
    write_jsonl_data as write_jsonl, load_json_or_jsonl, write_json_or_jsonl
)

# Aliases for backward compatibility
load_jsonl = read_jsonl
load_json = read_json


# Convert JSON to CSV or Excel
def convert_json_to_excel(file_name: str) -> str:
    """Convert JSON file to Excel format.

    Note: Requires pandas and openpyxl to be installed.
    Install with: pip install yueutils[excel]

    Args:
        file_name: Input JSON file path

    Returns:
        Output Excel file path

    Raises:
        ImportError: If pandas or openpyxl is not installed
    """
    try:
        import pandas as pd
    except ImportError:
        raise ImportError(
            "pandas is required for Excel conversion. "
            "Install it with: pip install yueutils[excel]"
        )

    data = read_json(file_name)
    df = pd.DataFrame(data)
    f_output = str(Path(file_name).with_suffix(".xlsx"))

    try:
        df.to_excel(f_output, index=False)
    except ImportError:
        raise ImportError(
            "openpyxl is required for Excel export. "
            "Install it with: pip install yueutils[excel]"
        )

    logger.info(f"Saved file as: {f_output}")
    return f_output


def convert_json_to_csv(file_name: str, use_pandas: bool = False) -> str:
    """Convert JSON file to CSV format.

    By default, uses built-in csv module (lightweight).
    Set use_pandas=True to use pandas (requires pandas installation).

    Args:
        file_name: Input JSON file path
        use_pandas: Whether to use pandas (default: False)

    Returns:
        Output CSV file path

    Raises:
        ImportError: If use_pandas=True but pandas is not installed
    """
    data = read_json(file_name)
    f_output = str(Path(file_name).with_suffix(".csv"))

    if use_pandas:
        try:
            import pandas as pd
        except ImportError:
            raise ImportError(
                "pandas is required when use_pandas=True. "
                "Install it with: pip install yueutils[excel] "
                "or set use_pandas=False to use built-in csv module"
            )
        df = pd.DataFrame(data)
        df.to_csv(f_output, index=False)
    else:
        # Use built-in csv module (lightweight)
        if not data:
            logger.warning(f"No data to write to {f_output}")
            with open(f_output, 'w', encoding='utf-8', newline='') as f:
                pass
            return f_output

        # Get all unique keys from all records
        fieldnames = []
        for record in data:
            if isinstance(record, dict):
                for key in record.keys():
                    if key not in fieldnames:
                        fieldnames.append(key)

        with open(f_output, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    logger.info(f"Saved file as: {f_output}")
    return f_output


def hf_dataset_to_json(dataset) -> List[Dict[str, Any]]:
    """Convert HuggingFace dataset to list of dictionaries.

    Note: This function requires pandas for conversion.
    Install with: pip install yueutils[excel]

    Args:
        dataset: HuggingFace dataset object

    Returns:
        List of dictionaries

    Raises:
        ImportError: If pandas is not installed
    """
    try:
        import pandas as pd
    except ImportError:
        raise ImportError(
            "pandas is required for HuggingFace dataset conversion. "
            "Install it with: pip install yueutils[excel]"
        )

    df = pd.DataFrame(dataset)
    return df.to_dict(orient="records")


# Alias for backward compatibility
hg_dataset_to_json = hf_dataset_to_json


# Model parameter counting utilities
def count_trainable_parameters(model) -> int:
    """Count the number of trainable parameters in a PyTorch model.

    Args:
        model: PyTorch model

    Returns:
        Number of trainable parameters
    """
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def count_no_trainable_parameters(model) -> int:
    """Count the number of non-trainable parameters in a PyTorch model.

    Args:
        model: PyTorch model

    Returns:
        Number of non-trainable parameters
    """
    return sum(p.numel() for p in model.parameters() if not p.requires_grad)


def count_parameters(model) -> int:
    """Count the total number of parameters in a PyTorch model.

    Args:
        model: PyTorch model

    Returns:
        Total number of parameters
    """
    return sum(p.numel() for p in model.parameters())


# Video frame utilities
def get_n_frames(start: int, end: int, n: int) -> List[int]:
    """Get N evenly spaced frame indices between start and end.

    Args:
        start: Starting frame index
        end: Ending frame index
        n: Number of frames to extract

    Returns:
        List of N evenly spaced frame indices
    """
    if n <= 1:
        return [start]
    step = (end - start) / (n - 1)
    return [int(start + step * i) for i in range(n)]


# Filename generation utilities
def generate_filename(
    data_source: str,
    from_model: str,
    date: Optional[datetime] = None,
    data: Optional[List] = None,
    comment: Optional[str] = None,
    is_raw: bool = False,
    additional_info: Optional[str] = None,
    extension: str = "json"
) -> str:
    """Generate standardized filename following naming conventions.

    Args:
        data_source: Data source or prompt origin
        from_model: Model name that generated the data
        date: Date for the file (YYYYMMDD string or datetime object). Defaults to now.
        data: Optional data list (used to add sample count to filename)
        comment: Optional comment to add to filename
        is_raw: Whether to mark file as raw data
        additional_info: Optional additional information
        extension: File extension (default: "json")

    Returns:
        Generated filename string

    Example:
        >>> generate_filename("wiki", "gpt4", comment="test", data=[1,2,3])
        '20260313_wiki_from-gpt4_comment-test_3.json'
    """
    if date is None:
        date = datetime.now()

    # Convert datetime to string
    if isinstance(date, datetime):
        date_str = date.strftime("%Y%m%d")
    else:
        date_str = str(date)

    # Build filename components
    from_model = f"from-{from_model}"
    filename_elements = [date_str, data_source, from_model]

    if additional_info:
        filename_elements.append(additional_info)
    if is_raw:
        filename_elements.append("raw")

    # Add comment if provided
    if comment:
        # Ensure comment contains only valid filename characters
        safe_comment = "".join([c for c in comment if c.isalnum() or c in ("_", "-")])
        filename_elements.append(f"comment-{safe_comment}")

    # Replace underscores with hyphens
    filename_elements = [elem.replace("_", "-") for elem in filename_elements]

    # Add data count if provided
    if data:
        filename = "_".join(filename_elements) + f"_{len(data)}.{extension}"
    else:
        filename = "_".join(filename_elements) + f".{extension}"

    return filename


def write_json_clean(data: List[Dict[str, Any]], f_save_path: str, f_save_name: str) -> None:
    """Write JSON data to a file with combined path.

    Args:
        data: Data to write
        f_save_path: Directory path
        f_save_name: Filename

    Example:
        >>> write_json_clean([{"a": 1}], "/tmp", "data.json")
    """
    f_output = os.path.join(f_save_path, f_save_name)
    write_json(data, f_output=f_output)


if __name__ == "__main__":
    pass
