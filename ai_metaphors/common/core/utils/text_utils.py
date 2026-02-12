from __future__ import annotations

import json
import re
from pathlib import Path


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
    :return: A dictionary representing the extracted JSON object if valid JSON is found and decoded successfully,
            otherwise None.
    """
    json_pattern = r"```json(.*?)```"
    match = re.search(json_pattern, text, re.DOTALL)
    if match:
        json_content = match.group(1)
        try:
            return json.loads(json_content)
        except json.JSONDecodeError:
            return text
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def extract_content(input_string: str) -> str:
    # Regex pattern to match content inside triple backticks
    pattern = r"```(.*?)```"
    match = re.search(pattern, input_string, re.DOTALL)

    # If a match is found, return the content inside backticks
    if match:
        return match.group(1)
    # If no match, return the whole string
    return input_string.strip()

def extract_steps_from_js(file_path: Path) -> str | None:
    # Read the file content
    file_content = file_path.read_text()
    # Define the regex pattern
    pattern = r'stepExplanations\s*=\s*\[(.*?)\];'
    # Perform regex search with the DOTALL flag to include newlines
    match = re.search(pattern, file_content, re.DOTALL)
    if match:
        # Extract and clean the stepExplanations content
        step_explanations = match.group(1).strip()
        # Return the list of step explanations as a Python list
        explanations =  [
            line.strip().strip(",")
            for line in step_explanations.splitlines() if line.strip()
        ]
        return "\n".join(
            f"{idx + 1}. {explanation}"
            for idx, explanation in enumerate(explanations)
        )
    else:
        print("No stepExplanations array found!")
        return None

def extract_code_from_html(file_path: Path) -> str | None:
    # Read the HTML file content
    file_content = file_path.read_text()
    # Regex pattern to capture content within the <code> ... </code> tag
    pattern = r'<code>(.*?)</code>'
    # Perform regex search with the DOTALL flag to include newlines
    match = re.search(pattern, file_content, re.DOTALL)

    if match:
        # Extract the code with indentation preserved
        code_content = match.group(1).strip()
        # Clean the code by removing <span> tags and their attributes
        cleaned_code = re.sub(r'<span[^>]*?>', '', code_content)  # Remove opening <span> tags
        cleaned_code = re.sub(r'</span>', '', cleaned_code)  # Remove closing </span> tags
        return cleaned_code.strip()
    else:
        print("No <code> block found in the HTML file!")
        return None