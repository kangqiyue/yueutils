"""Tests for JSON/JSONL utilities."""

import pytest
from pathlib import Path
from yueutils.data.utils_json import (
    read_json,
    write_json,
    read_jsonl_data,
    write_jsonl_data,
    load_json_or_jsonl,
    write_json_or_jsonl,
)


class TestJSONUtils:
    """Test JSON read/write functions."""

    def test_write_and_read_json(self, temp_dir, sample_data):
        """Test writing and reading JSON files."""
        json_file = temp_dir / "test.json"

        # Write
        write_json(sample_data, str(json_file))
        assert json_file.exists()

        # Read
        loaded_data = read_json(str(json_file))
        assert loaded_data == sample_data
        assert len(loaded_data) == 3

    def test_write_and_read_jsonl(self, temp_dir, sample_data):
        """Test writing and reading JSONL files."""
        jsonl_file = temp_dir / "test.jsonl"

        # Write
        write_jsonl_data(sample_data, str(jsonl_file))
        assert jsonl_file.exists()

        # Read
        loaded_data = read_jsonl_data(str(jsonl_file))
        assert loaded_data == sample_data
        assert len(loaded_data) == 3

    def test_load_json_or_jsonl_with_json(self, temp_dir, sample_data):
        """Test load_json_or_jsonl with .json file."""
        json_file = temp_dir / "test.json"
        write_json(sample_data, str(json_file))

        loaded_data = load_json_or_jsonl(str(json_file))
        assert loaded_data == sample_data

    def test_load_json_or_jsonl_with_jsonl(self, temp_dir, sample_data):
        """Test load_json_or_jsonl with .jsonl file."""
        jsonl_file = temp_dir / "test.jsonl"
        write_jsonl_data(sample_data, str(jsonl_file))

        loaded_data = load_json_or_jsonl(str(jsonl_file))
        assert loaded_data == sample_data

    def test_load_json_or_jsonl_invalid_extension(self, temp_dir):
        """Test load_json_or_jsonl with invalid extension."""
        invalid_file = temp_dir / "test.txt"
        invalid_file.touch()

        with pytest.raises(NotImplementedError):
            load_json_or_jsonl(str(invalid_file))

    def test_write_json_or_jsonl_with_json(self, temp_dir, sample_data):
        """Test write_json_or_jsonl with .json extension."""
        json_file = temp_dir / "output.json"

        write_json_or_jsonl(sample_data, str(json_file))
        assert json_file.exists()

        loaded_data = read_json(str(json_file))
        assert loaded_data == sample_data

    def test_write_json_or_jsonl_with_jsonl(self, temp_dir, sample_data):
        """Test write_json_or_jsonl with .jsonl extension."""
        jsonl_file = temp_dir / "output.jsonl"

        write_json_or_jsonl(sample_data, str(jsonl_file))
        assert jsonl_file.exists()

        loaded_data = read_jsonl_data(str(jsonl_file))
        assert loaded_data == sample_data

    def test_case_insensitive_extension(self, temp_dir, sample_data):
        """Test that file extension checking is case-insensitive."""
        json_file = temp_dir / "test.JSON"
        write_json(sample_data, str(json_file))

        loaded_data = load_json_or_jsonl(str(json_file))
        assert loaded_data == sample_data
