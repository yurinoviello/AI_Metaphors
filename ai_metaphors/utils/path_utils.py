import logging
from pathlib import Path


def process_executable_path(executable_path: str, required_tools: tuple = ("manim", "pylint", "python")) -> Path:
    if not Path(executable_path).is_dir():
        msg = (
            f"The executable path '{executable_path}' does not exist."
            "Please provide a valid path to the executable directory."
        )
        raise ValueError(msg)
    # Check if required dependencies are installed within the executable path
    for tool in required_tools:
        tool_path = Path(executable_path) / tool
        if not tool_path.exists() or not tool_path.is_file():
            msg = f"The required tool '{tool}' is not found or not executable within the path '{executable_path}'."
            raise OSError(msg)
    return Path(executable_path).absolute()


def process_working_dir(working_dir: str) -> Path:
    if not Path(working_dir).exists():
        logging.warning(
            "The working directory '%s' does not exist. Creating the default './animations' directory.",
            working_dir,
        )
        Path(working_dir).mkdir(parents=True, exist_ok=True)
    return Path(working_dir).absolute()
