from argparse import ArgumentTypeError
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from ai_metaphors.common.core.utils import path_utils


class TestProcessExecutablePath(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory to simulate an "executable" path
        self.temp_dir = tempfile.mkdtemp()
        self.required_tools = ("manim", "pylint", "python")

        # Create empty files named after the required tools (simulating executables)
        for tool in self.required_tools:
            tool_path = Path(self.temp_dir) / tool
            tool_path.touch()

    def tearDown(self):
        # Remove the temporary directory after each test
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_valid_executable_path(self):
        """Test that process_executable_path returns a Path object if all required tools are present."""
        result = path_utils.process_bin_directory(self.temp_dir, self.required_tools)
        self.assertTrue(Path(result).is_absolute(), "Returned path should be absolute")
        self.assertTrue(Path(result).exists(), "Returned path should exist")

    def test_invalid_path_raises_value_error(self):
        """Test that a non-existing path raises a ValueError."""
        with self.assertRaises(ValueError):
            path_utils.process_bin_directory("/invalid/path", self.required_tools)

    def test_missing_tool_raises_os_error(self):
        """Test that missing a required tool raises an OSError."""
        for tool in self.required_tools:
            with self.subTest(missing_tool=tool):
                # Remove one tool from the temp_dir
                missing_tool = Path(self.temp_dir) / tool
                if missing_tool.exists():
                    missing_tool.unlink()

                with self.assertRaises(ArgumentTypeError):
                    path_utils.process_bin_directory(self.temp_dir, self.required_tools)

                # Restore the missing tool for the next subTest
                missing_tool.touch()


class TestProcessWorkingDir(unittest.TestCase):
    def test_working_dir_exists(self):
        """
        Test that if the working directory already exists, process_working_dir
        returns its absolute path without creating a new directory.
        """
        with tempfile.TemporaryDirectory() as existing_dir:
            result = path_utils.process_working_dir(existing_dir)
            self.assertTrue(Path(result).is_absolute(), "Returned path should be absolute")
            self.assertTrue(Path(existing_dir).exists(), "Existing directory should still exist")

    def test_working_dir_creates_if_not_existing(self):
        """
        Test that if the working directory does not exist, it is automatically created
        and a warning is logged.
        """
        with tempfile.TemporaryDirectory() as base_dir:
            non_existing_dir = str(Path(base_dir) / "nested" / "dir")

            with (
                self.subTest(non_existing_dir=non_existing_dir),
                patch("ai_metaphors.common.utils.path_utils.logging.warning") as mock_warning,
            ):
                result = path_utils.process_working_dir(non_existing_dir)

                # Check that process_working_dir logs a warning
                mock_warning.assert_called_once()

                # Check that the directory is created
                self.assertTrue(Path(non_existing_dir).exists(), "Non-existing directory should be created")
                self.assertTrue(Path(result).is_absolute(), "Returned path should be absolute")

    def test_process_working_dir_returns_absolute_path(self):
        """
        Test that process_working_dir always returns an absolute path, even if
        a relative path is provided.
        """
        relative_dirs = ["relative_path_dir", "./another_relative_path"]

        for relative_dir in relative_dirs:
            with self.subTest(relative_dir=relative_dir):
                result = path_utils.process_working_dir(relative_dir)
                self.assertTrue(Path(result).is_absolute(), "Returned path should be absolute")
                self.assertTrue(Path(result).exists(), "Directory should be created if it did not exist")
                # Clean up after the test
                shutil.rmtree(Path(result), ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
