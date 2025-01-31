import logging
from argparse import ArgumentTypeError
from pathlib import Path


def process_bin_directory(bin_directory: str, required_tools: tuple = ("manim", "pylint", "python")) -> Path:
    if not Path(bin_directory).is_dir():
        msg = (
            f"The bin directory '{bin_directory}' does not exist."
            "Please provide a valid path to the bin directory."
        )
        raise ValueError(msg)
    # Check if required dependencies are installed within the executable path
    for tool in required_tools:
        tool_path = Path(bin_directory) / tool
        if not tool_path.exists() or not tool_path.is_file():
            msg = f"The required tool '{tool}' is not found within the path '{bin_directory}'."
            raise ArgumentTypeError(msg)
    return Path(bin_directory).absolute()


def process_working_dir(working_dir: str) -> Path:
    if not Path(working_dir).exists():
        logging.warning(
            "The working directory '%s' does not exist. The directory will be created.",
            working_dir,
        )
        Path(working_dir).mkdir(parents=True, exist_ok=True)
    return Path(working_dir).absolute()
