"""Tests for Parquet utilities."""

import pytest
from pathlib import Path
from yueutils.data.utils_polars import (
    read_parquet,
    write_parquet,
    load_json_or_parquet,
    write_json_or_parquet,
)
from yueutils.data.utils_json import write_json


class TestParquetUtils:
    """Test Parquet read/write functions."""

    def test_write_and_read_parquet(self, temp_dir, sample_data):
        """Test writing and reading Parquet files."""
        parquet_file = temp_dir / "test.parquet"

        # Write
        write_parquet(sample_data, str(parquet_file))
        assert parquet_file.exists()

        # Read
        loaded_data = read_parquet(str(parquet_file))
        assert len(loaded_data) == 3

        # Convert to list of dicts for comparison
        result = loaded_data.to_dicts()
        assert result == sample_data

    def test_write_parquet_with_demo(self, temp_dir, sample_data):
        """Test that demo JSON file is created."""
        parquet_file = temp_dir / "test.parquet"

        write_parquet(sample_data, str(parquet_file), demo_num=2)

        # Check demo file exists
        demo_file = temp_dir / "test_demo.json"
        assert demo_file.exists()

    def test_write_parquet_without_demo(self, temp_dir, sample_data):
        """Test writing without demo file."""
        parquet_file = temp_dir / "test.parquet"

        write_parquet(sample_data, str(parquet_file), demo_num=None)

        # Check demo file doesn't exist
        demo_file = temp_dir / "test_demo.json"
        assert not demo_file.exists()

    def test_load_json_or_parquet_with_json(self, temp_dir, sample_data):
        """Test load_json_or_parquet with JSON file."""
        json_file = temp_dir / "test.json"
        write_json(sample_data, str(json_file))

        loaded_data = load_json_or_parquet(str(json_file))
        assert loaded_data == sample_data

    def test_load_json_or_parquet_with_parquet(self, temp_dir, sample_data):
        """Test load_json_or_parquet with Parquet file."""
        parquet_file = temp_dir / "test.parquet"
        write_parquet(sample_data, str(parquet_file))

        loaded_data = load_json_or_parquet(str(parquet_file))
        assert len(loaded_data) == 3

    def test_auto_convert_large_data_to_parquet(self, temp_dir, large_sample_data):
        """Test automatic conversion to Parquet for large datasets."""
        json_file = temp_dir / "large.json"

        # Should auto-convert to .parquet
        final_path = write_json_or_parquet(large_sample_data, str(json_file))

        assert final_path.endswith(".parquet")
        parquet_file = Path(final_path)
        assert parquet_file.exists()
        assert not json_file.exists()

    def test_auto_convert_small_data_to_json(self, temp_dir, sample_data):
        """Test automatic conversion to JSON for small datasets."""
        parquet_file = temp_dir / "small.parquet"

        # Should auto-convert to .json
        final_path = write_json_or_parquet(sample_data, str(parquet_file))

        assert final_path.endswith(".json")
        json_file = Path(final_path)
        assert json_file.exists()
        assert not parquet_file.exists()
