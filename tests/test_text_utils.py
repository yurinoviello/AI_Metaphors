import unittest

from ai_metaphors.core.utils import text_utils


class TestUtilsExtractContent(unittest.TestCase):
    def setUp(self):
        self.test_cases = [
            ("```\nThis is some text inside backticks.\n```", "\nThis is some text inside backticks.\n"),
            ("This is some text without backticks.", "This is some text without backticks."),
            ("", ""),
        ]

    def test_extract_content(self):
        for input_string, expected_result in self.test_cases:
            with self.subTest(input_string=input_string):
                result = text_utils.extract_content(input_string)
                self.assertEqual(result, expected_result)


class TestUtilsExtractJSON(unittest.TestCase):
    def setUp(self):
        self.test_cases = [
            (
                """This is a sample text.
                ```json
                {
                    "name": "John Boe",
                    "email": "johnboe@example.com"
                }
                ```""",
                {"name": "John Boe", "email": "johnboe@example.com"},
            ),
            (
                """This is a sample text.
                ```json
                {
                    "name": "John Boe",
                    "email: "johnboe@example.com"
                }
                ```""",
                None,
            ),
            ("This is a sample text with no json object.", None),
            (
                """test for empty json
                ```json
                {}
                ```""",
                {},
            ),
            (
                """This is a sample text.
                ```json
                {
                    "name": "John Boe",
                    "email": "johnboe@example.com"
                }
                ```
                This is another json object.
                ```json
                {
                    "name": "Jane Boe",
                    "email": "janeboe@example.com"
                }
                ```""",
                {"name": "John Boe", "email": "johnboe@example.com"},
            ),
        ]

    def test_extract_json(self):
        for text, expected in self.test_cases:
            with self.subTest(text=text):
                result = text_utils.extract_json(text)
                self.assertEqual(result, expected)


class TestUtilsExtractPythonCode(unittest.TestCase):
    def setUp(self):
        self.test_cases = [
            (
                "Here is some Python code:\n```python\nprint('Hello, World!')\n```",
                "print('Hello, World!')",
            ),
            (
                "Here is some text without Python code: print('Hello, World!')",
                None,
            ),
            (
                "Multiple python code blocks \n```python\nprint('Block 1')\n```\n```python\nprint('Block 2')\n```",
                "print('Block 1')",
            ),
            (
                "Python code without 'python' after backticks \n```\na = 5\nb = 10\nprint(a+b)\n```",
                "a = 5\nb = 10\nprint(a+b)",
            ),
            ("", None),
        ]

    def test_extract_python_code(self):
        for input_text, expected in self.test_cases:
            with self.subTest(input_text=input_text):
                result = text_utils.extract_python_code(input_text)
                self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
