import jsonlines
import json
from pathlib import Path
from typing import List, Dict, Any
from loguru import logger


# JSON/JSONL utilities
def read_jsonl_data(f_input: str) -> List[Dict[str, Any]]:
    """Read data from a JSONL file.

    Args:
        f_input: Input JSONL file path

    Returns:
        List of dictionaries
    """
    data = []
    with open(f_input, 'r', encoding="utf-8") as fd:
        for line in jsonlines.Reader(fd):
            data.append(line)
    logger.info(f"Loaded {len(data)} records from {f_input}")
    return data


def write_jsonl_data(res: List[Dict[str, Any]], f_output: str) -> None:
    """Write data to a JSONL file.

    Args:
        res: List of dictionaries to write
        f_output: Output JSONL file path
    """
    with jsonlines.open(f_output, 'w') as writer:
        writer.write_all(res)
    logger.info(f"Wrote {len(res)} records to {f_output}")


def read_json(f_input: str) -> List[Dict[str, Any]]:
    """Read data from a JSON file.

    Args:
        f_input: Input JSON file path

    Returns:
        List of dictionaries or dict
    """
    with open(f_input, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        logger.info(f"Loaded {len(data)} records from {f_input}")
    else:
        logger.info(f"Loaded data from {f_input}")
    return data


def write_json(res: List[Dict[str, Any]], f_output: str) -> None:
    """Write data to a JSON file.

    Args:
        res: Data to write (list or dict)
        f_output: Output JSON file path
    """
    with open(f_output, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    if isinstance(res, list):
        logger.info(f"Wrote {len(res)} records to {f_output}")
    else:
        logger.info(f"Wrote data to {f_output}")

# Aliases for backward compatibility
load_jsonl = read_jsonl_data
read_jsonl = read_jsonl_data
write_jsonl = write_jsonl_data
load_json = read_json


def load_json_or_jsonl(f_input: str) -> List[Dict[str, Any]]:
    """Load data from JSON or JSONL file.

    Args:
        f_input: Input file path (.json or .jsonl)

    Returns:
        List of dictionaries

    Raises:
        NotImplementedError: If file extension is not .json or .jsonl
    """
    suffix = Path(f_input).suffix.lower()

    if suffix == ".jsonl":
        return read_jsonl_data(f_input)
    elif suffix == ".json":
        return read_json(f_input)
    else:
        raise NotImplementedError(f"ERROR, must be .json or .jsonl, but got {f_input}")


def write_json_or_jsonl(res: List[Dict[str, Any]], f_output: str) -> None:
    """Write data to JSON or JSONL file.

    Args:
        res: Data to write
        f_output: Output file path (.json or .jsonl)

    Raises:
        NotImplementedError: If file extension is not .json or .jsonl
    """
    suffix = Path(f_output).suffix.lower()

    if suffix == ".jsonl":
        write_jsonl(res, f_output)
    elif suffix == ".json":
        write_json(res, f_output)
    else:
        raise NotImplementedError(f"ERROR, must be .json or .jsonl, but got {f_output}")


