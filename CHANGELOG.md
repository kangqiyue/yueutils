# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-03-13

### Added
- ✅ Comprehensive unit test suite with 40+ tests
- 📦 Optional `[excel]` dependency group for pandas/openpyxl
- 🔧 Built-in CSV conversion using Python's csv module (no pandas required)
- 📝 Test fixtures and conftest.py for pytest

### Changed
- **BREAKING**: `pandas` is now an optional dependency
  - Install with `pip install yueutils[excel]` for Excel features
  - `convert_json_to_csv()` now defaults to built-in csv module
  - Set `use_pandas=True` parameter to use pandas (if installed)
- **BREAKING**: Better error messages when optional dependencies are missing
- 🔧 File extension checking now uses `pathlib.Path` for cross-platform compatibility
- 🔧 File path operations now use `Path.with_suffix()` instead of string replacement
- 🎯 All file extension checks are now case-insensitive

### Fixed
- 🐛 File extension checking is now platform-independent (Windows/Linux/macOS)
- 🐛 Demo file generation in Parquet writer now uses proper path manipulation
- 🐛 Extension checking properly handles uppercase extensions (.JSON, .JSONL)

### Removed
- ❌ Removed unused `toml` dependency
- ❌ Removed unused `import time` from utils.py
- ❌ Removed unused `from functools import wraps` from cleaner.py
- 📉 Reduced installation size by ~200MB (pandas now optional)

## [0.2.0] - 2026-03-13

### Added
- Type hints throughout the entire codebase for better IDE support
- Comprehensive docstrings for all public functions
- Modern Python packaging with `pyproject.toml`
- `.gitignore` file with Python-specific ignore patterns
- `requirements.txt` and `requirements-dev.txt` for dependency management
- `CHANGELOG.md` to track version changes
- Better error messages and input validation
- Return values for functions that create files (return file paths)

### Changed
- **BREAKING**: `write_data()` now returns the output file path
- **BREAKING**: `write_json_or_parquet()` now returns the output file path
- Unified logging system using `loguru` instead of mixed `print` statements
- Improved project structure with proper package configuration using `find_packages()`
- Updated `setup.py` with complete dependency list and metadata
- Better handling of edge cases (e.g., `get_n_frames` with n=1)
- Code quality improvements across all modules

### Fixed
- **Critical**: Fixed `endwith` → `endswith` typo in `write_json_or_jsonl` function
- **Critical**: Fixed `__mian__` → `__main__` typo in utils.py
- Fixed variable name typo: `f_outupt` → `f_output` in conversion functions
- Fixed CSV/Excel export to exclude index column by default

### Removed
- Duplicate code between `utils.py` and `data/utils_json.py`
- Unused and commented-out code in setup.py

### Refactored
- Consolidated JSON/JSONL utilities into `data/utils_json.py`
- Updated imports in `__init__.py` for cleaner API surface
- Better separation of concerns between modules
- Improved code organization in `data/__init__.py`

## [0.1.0] - Initial Release

### Added
- Basic JSON/JSONL read/write utilities
- Parquet support using Polars
- HuggingFace Dataset integration
- Data conversion utilities (JSON to CSV/Excel)
- PyTorch model parameter counting
- Time and length counter decorators
- Filename generation utilities
- Distributed training utilities (dist_utils.py)
