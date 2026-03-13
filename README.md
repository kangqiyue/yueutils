# yueutils

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-AFL--3.0-green)](LICENSE)

Common utility functions for Python projects, focusing on data processing with JSON, JSONL, and Parquet formats.

## Features

- 🚀 **Simple API**: Easy-to-use functions for common data operations
- 📊 **Multiple Formats**: Support for JSON, JSONL, and Parquet files
- ⚡ **Smart Auto-conversion**: Automatically optimizes file format based on data size
- 🔧 **Type Hints**: Full type annotations for better IDE support
- 📝 **Logging**: Built-in logging with loguru for better debugging

## Installation

```bash
pip install yueutils
```

### Development Installation

```bash
git clone https://github.com/kangqiyue/yueutils.git
cd yueutils
pip install -e ".[dev]"
```

### Optional Dependencies

For Excel conversion and pandas integration:

```bash
pip install yueutils[excel]
```

For deep learning features (distributed training, model utilities):

```bash
pip install yueutils[deeplearning]
```

## Quick Start

### Basic Usage

```python
from yueutils import load_data, write_data

# Load data (supports .json, .jsonl, .parquet)
data = load_data("input.json")

# Process your data
processed_data = [{"id": i, "value": item["value"] * 2} for i, item in enumerate(data)]

# Write data (auto-converts to parquet for large datasets)
write_data(processed_data, "output.json")
```

### Working with Different Formats

```python
from yueutils import read_json, read_jsonl, read_parquet
from yueutils import write_json, write_jsonl, write_parquet

# JSON
data = read_json("data.json")
write_json(data, "output.json")

# JSONL
data = read_jsonl("data.jsonl")
write_jsonl(data, "output.jsonl")

# Parquet (efficient for large datasets)
data = read_parquet("data.parquet")
write_parquet(data, "output.parquet")
```

### Data Conversion

```python
from yueutils import convert_json_to_csv, convert_json_to_excel

# Convert JSON to CSV (lightweight, no extra dependencies)
convert_json_to_csv("data.json")  # Creates data.csv

# Convert JSON to CSV using pandas (requires yueutils[excel])
convert_json_to_csv("data.json", use_pandas=True)

# Convert JSON to Excel (requires yueutils[excel])
convert_json_to_excel("data.json")  # Creates data.xlsx
```

### HuggingFace Datasets

```python
from datasets import load_dataset
from yueutils import hf_dataset_to_json, write_data

# Load HuggingFace dataset
dataset = load_dataset("squad", split="train[:100]")

# Convert to JSON format
data = hf_dataset_to_json(dataset)

# Save
write_data(data, "squad_sample.json")
```

### Decorators

```python
from yueutils import time_counter, length_counter_before_after

@time_counter
def process_data(data):
    # Your processing logic
    return [item for item in data if item["value"] > 0]

@length_counter_before_after
def filter_data(self, data):
    # Automatically logs input/output lengths
    return [item for item in data if item["valid"]]
```

### PyTorch Model Utilities

```python
from yueutils import count_parameters, count_trainable_parameters

# Count model parameters
total_params = count_parameters(model)
trainable_params = count_trainable_parameters(model)

print(f"Total: {total_params:,} | Trainable: {trainable_params:,}")
```

### Filename Generation

```python
from yueutils import generate_filename

# Generate standardized filename
filename = generate_filename(
    data_source="wiki",
    from_model="gpt4",
    comment="test",
    data=my_data  # Adds sample count
)
# Output: 20260313_wiki_from-gpt4_comment-test_1000.json
```

## API Reference

### Core Functions

- `load_data(f_input: str)` - Load data from JSON/JSONL/Parquet
- `write_data(data: list, f_output: str)` - Write data with auto-optimization

### JSON/JSONL Functions

- `read_json(f_input: str)` - Read JSON file
- `write_json(data: list, f_output: str)` - Write JSON file
- `read_jsonl(f_input: str)` - Read JSONL file
- `write_jsonl(data: list, f_output: str)` - Write JSONL file

### Parquet Functions

- `read_parquet(f_input: str)` - Read Parquet file (returns Polars DataFrame)
- `write_parquet(data: list, f_output: str)` - Write Parquet file

### Conversion Functions

- `convert_json_to_csv(file_name: str)` - Convert JSON to CSV
- `convert_json_to_excel(file_name: str)` - Convert JSON to Excel
- `hf_dataset_to_json(dataset)` - Convert HuggingFace Dataset to JSON

### Model Utilities

- `count_parameters(model)` - Count total model parameters
- `count_trainable_parameters(model)` - Count trainable parameters
- `count_no_trainable_parameters(model)` - Count non-trainable parameters

### Decorators

- `@time_counter` - Measure function execution time
- `@length_counter` - Log output data length
- `@length_counter_before_after` - Log input and output data lengths

### Other Utilities

- `get_n_frames(start: int, end: int, n: int)` - Get N evenly spaced frame indices
- `generate_filename(...)` - Generate standardized filenames

## Auto-Optimization

The library automatically optimizes file formats based on data size:

- **< 20,000 records**: Uses JSON for better readability
- **≥ 20,000 records**: Automatically converts to Parquet for better performance

```python
# Automatically converts to parquet for large datasets
large_data = [{"id": i} for i in range(50000)]
write_data(large_data, "output.json")  # Actually saves as output.parquet
```

## Requirements

### Core Dependencies

- Python >= 3.8
- jsonlines >= 3.0.0
- polars >= 1.4.1
- datasets >= 2.21.0
- loguru >= 0.6.0

### Optional Dependencies

- **excel**: pandas >= 1.3.0, openpyxl >= 3.0.0 (for Excel and advanced CSV conversion)
- **deeplearning**: torch >= 2.0.0, deepspeed >= 0.10.0 (for distributed training utilities)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the Academic Free License v3.0 (AFL-3.0).

## Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=yueutils --cov-report=html
```

## Changelog

### v0.3.0 (2026-03-13) - Latest

**Major improvements:**
- 🚀 **Lightweight Core**: Removed unused dependencies (toml), made pandas optional
- 🔧 **Cross-platform Fix**: Using pathlib for robust file extension checking
- ✅ **Test Coverage**: Added comprehensive unit tests
- 📦 **Modular Install**: Optional dependencies for excel and deeplearning features

**Breaking Changes:**
- `pandas` is now optional - install with `pip install yueutils[excel]` if needed
- `convert_json_to_csv()` now defaults to built-in csv module (set `use_pandas=True` for old behavior)

**Bug Fixes:**
- Fixed file extension checking to be case-insensitive and platform-independent
- Removed unused imports (toml, time, functools.wraps)

### v0.2.0 (2026-03-13)

- ✨ Added type hints throughout the codebase
- 🐛 Fixed critical bugs (`endwith` → `endswith`, `__mian__` → `__main__`)
- 🔧 Improved project structure with proper package configuration
- 📝 Added comprehensive documentation
- ♻️ Refactored to eliminate code duplication
- 🎨 Unified logging with loguru
- 📦 Added modern Python packaging (pyproject.toml)
- ✅ Better error messages and validation

### v0.1.0

- Initial release
