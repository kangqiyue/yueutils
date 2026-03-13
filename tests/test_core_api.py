"""Tests for core API (load_data, write_data)."""

import pytest
from pathlib import Path
from yueutils import load_data, write_data


class TestCoreAPI:
    """Test core load_data and write_data functions."""

    def test_load_data_json(self, temp_dir, sample_data):
        """Test load_data with JSON file."""
        from yueutils import write_json

        json_file = temp_dir / "test.json"
        write_json(sample_data, str(json_file))

        loaded_data = load_data(str(json_file))
        assert loaded_data == sample_data

    def test_load_data_jsonl(self, temp_dir, sample_data):
        """Test load_data with JSONL file."""
        from yueutils import write_jsonl

        jsonl_file = temp_dir / "test.jsonl"
        write_jsonl(sample_data, str(jsonl_file))

        loaded_data = load_data(str(jsonl_file))
        assert loaded_data == sample_data

    def test_load_data_parquet(self, temp_dir, sample_data):
        """Test load_data with Parquet file."""
        from yueutils import write_parquet

        parquet_file = temp_dir / "test.parquet"
        write_parquet(sample_data, str(parquet_file))

        loaded_data = load_data(str(parquet_file))
        assert len(loaded_data) == 3

    def test_load_data_invalid_extension(self, temp_dir):
        """Test load_data with unsupported file type."""
        txt_file = temp_dir / "test.txt"
        txt_file.touch()

        with pytest.raises(NotImplementedError):
            load_data(str(txt_file))

    def test_write_data_json(self, temp_dir, sample_data):
        """Test write_data with .json extension."""
        json_file = temp_dir / "output.json"

        final_path = write_data(sample_data, str(json_file))
        assert final_path == str(json_file)
        assert Path(json_file).exists()

    def test_write_data_jsonl(self, temp_dir, sample_data):
        """Test write_data with .jsonl extension."""
        jsonl_file = temp_dir / "output.jsonl"

        final_path = write_data(sample_data, str(jsonl_file))
        assert final_path == str(jsonl_file)
        assert Path(jsonl_file).exists()

    def test_write_data_parquet(self, temp_dir, sample_data):
        """Test write_data with .parquet extension."""
        parquet_file = temp_dir / "output.parquet"

        final_path = write_data(sample_data, str(parquet_file))
        # Small data auto-converts to JSON
        assert final_path.endswith(".json")

    def test_write_data_auto_convert_large(self, temp_dir, large_sample_data):
        """Test write_data auto-converts large data to Parquet."""
        json_file = temp_dir / "large.json"

        final_path = write_data(large_sample_data, str(json_file))
        # Large data auto-converts to Parquet
        assert final_path.endswith(".parquet")
        assert Path(final_path).exists()

    def test_write_data_invalid_extension(self, temp_dir, sample_data):
        """Test write_data with unsupported file type."""
        txt_file = temp_dir / "output.txt"

        with pytest.raises(NotImplementedError):
            write_data(sample_data, str(txt_file))

    def test_round_trip_json(self, temp_dir, sample_data):
        """Test round-trip: write then read JSON."""
        json_file = temp_dir / "round_trip.json"

        write_data(sample_data, str(json_file))
        loaded_data = load_data(str(json_file))

        assert loaded_data == sample_data

    def test_case_insensitive_load(self, temp_dir, sample_data):
        """Test that load_data handles uppercase extensions."""
        from yueutils import write_json

        json_file = temp_dir / "test.JSON"
        write_json(sample_data, str(json_file))

        loaded_data = load_data(str(json_file))
        assert loaded_data == sample_data
