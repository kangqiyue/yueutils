# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
