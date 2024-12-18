from __future__ import annotations

import json
import re


def extract_python_code(text: str) -> str | None:
    """
    :param text: A string that may contain Python code block encapsulated within triple backticks.
    :return: Extracted Python code from the provided text, if found; otherwise, returns None.
    """
    pattern = re.compile(r"```(?:python)?\n(.*?)```", re.DOTALL)
    match = pattern.search(text)
    if match:
        return match.group(1).strip()
    return None


def extract_json(text: str) -> str | None:
    """
    :param text: A string that potentially contains a JSON object wrapped in triple backticks.
    :return: A dictionary representing the extracted JSON object if valid JSON is found and decoded successfully,otherwise None.
    """
    json_pattern = r"```json(.*?)```"
    match = re.search(json_pattern, text, re.DOTALL)
    if match:
        json_content = match.group(1)
        try:
            return json.loads(json_content)
        except json.JSONDecodeError:
            print("Invalid JSON found.")
            return None
    return None


def extract_content(input_string: str) -> str:
    # Regex pattern to match content inside triple backticks
    pattern = r"```(.*?)```"
    match = re.search(pattern, input_string, re.DOTALL)

    # If a match is found, return the content inside backticks
    if match:
        return match.group(1)
    # If no match, return the whole string
    return input_string.strip()
