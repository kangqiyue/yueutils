"""Tests for utility functions."""

import pytest
from pathlib import Path
from yueutils import (
    convert_json_to_csv,
    get_n_frames,
    generate_filename,
)


class TestConversionUtils:
    """Test data conversion utilities."""

    def test_convert_json_to_csv_builtin(self, temp_dir, sample_data):
        """Test JSON to CSV conversion with built-in csv module."""
        from yueutils import write_json

        json_file = temp_dir / "test.json"
        write_json(sample_data, str(json_file))

        # Convert using built-in csv module (default)
        csv_file = convert_json_to_csv(str(json_file), use_pandas=False)

        assert Path(csv_file).exists()
        assert csv_file.endswith(".csv")

        # Verify CSV content
        with open(csv_file, 'r') as f:
            content = f.read()
            assert "id,name,value" in content
            assert "Alice" in content
            assert "Bob" in content


class TestFrameUtils:
    """Test video frame utilities."""

    def test_get_n_frames_basic(self):
        """Test getting evenly spaced frames."""
        frames = get_n_frames(0, 100, 5)
        assert frames == [0, 25, 50, 75, 100]

    def test_get_n_frames_single(self):
        """Test getting single frame."""
        frames = get_n_frames(0, 100, 1)
        assert frames == [0]

    def test_get_n_frames_two(self):
        """Test getting two frames."""
        frames = get_n_frames(10, 20, 2)
        assert frames == [10, 20]

    def test_get_n_frames_uneven(self):
        """Test with numbers that don't divide evenly."""
        frames = get_n_frames(0, 10, 3)
        assert len(frames) == 3
        assert frames[0] == 0
        assert frames[-1] == 10


class TestFilenameGeneration:
    """Test filename generation utilities."""

    def test_generate_filename_basic(self):
        """Test basic filename generation."""
        from datetime import datetime

        date = datetime(2026, 3, 13)
        filename = generate_filename(
            data_source="wiki",
            from_model="gpt4",
            date=date
        )

        assert "20260313" in filename
        assert "wiki" in filename
        assert "from-gpt4" in filename
        assert filename.endswith(".json")

    def test_generate_filename_with_data_count(self):
        """Test filename generation with data count."""
        from datetime import datetime

        date = datetime(2026, 3, 13)
        data = [1, 2, 3, 4, 5]

        filename = generate_filename(
            data_source="test",
            from_model="model",
            date=date,
            data=data
        )

        assert "_5.json" in filename

    def test_generate_filename_with_comment(self):
        """Test filename generation with comment."""
        from datetime import datetime

        date = datetime(2026, 3, 13)
        filename = generate_filename(
            data_source="test",
            from_model="model",
            date=date,
            comment="experiment"
        )

        assert "comment-experiment" in filename

    def test_generate_filename_is_raw(self):
        """Test filename generation with raw flag."""
        from datetime import datetime

        date = datetime(2026, 3, 13)
        filename = generate_filename(
            data_source="test",
            from_model="model",
            date=date,
            is_raw=True
        )

        assert "raw" in filename

    def test_generate_filename_custom_extension(self):
        """Test filename generation with custom extension."""
        from datetime import datetime

        date = datetime(2026, 3, 13)
        filename = generate_filename(
            data_source="test",
            from_model="model",
            date=date,
            extension="parquet"
        )

        assert filename.endswith(".parquet")


class TestModelUtils:
    """Test PyTorch model utilities."""

    def test_count_parameters_mock(self):
        """Test parameter counting with mock model."""
        from yueutils import count_parameters

        class MockParameter:
            def __init__(self, size):
                self.size = size

            def numel(self):
                return self.size

        class MockModel:
            def parameters(self):
                return [
                    MockParameter(100),
                    MockParameter(200),
                    MockParameter(300),
                ]

        model = MockModel()
        total = count_parameters(model)
        assert total == 600
