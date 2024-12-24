import unittest

from ai_metaphors.utils import text_utils


class TestUtilsExtractContent(unittest.TestCase):
    def setUp(self):
        self.string_with_backticks = "```\nThis is some text inside backticks.\n```"
        self.string_without_backticks = "This is some text without backticks."
        self.empty_string = ""

    def test_extract_content_with_backticks(self):
        result = text_utils.extract_content(self.string_with_backticks)
        expected_result = "\nThis is some text inside backticks.\n"
        self.assertEqual(result, expected_result)

    def test_extract_content_without_backticks(self):
        result = text_utils.extract_content(self.string_without_backticks)
        self.assertEqual(result, self.string_without_backticks)

    def test_extract_content_empty_string(self):
        result = text_utils.extract_content(self.empty_string)
        self.assertEqual(result, self.empty_string)


class TestUtilsExtractJSON(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        """This method is called after each test"""

    def test_extract_json_valid(self):
        """Test case for valid json"""
        text = """This is a sample text.
                ```json
                {
                    "name": "John Doe",
                    "email": "johndoe@example.com"
                }
                ```"""
        expected = {
            "name": "John Doe",
            "email": "johndoe@example.com",
        }
        result = text_utils.extract_json(text)
        self.assertEqual(result, expected)

    def test_extract_json_invalid(self):
        """Test case for invalid json"""
        text = """This is a sample text.
                ```json
                {
                    "name": "John Doe",
                    "email: "johndoe@example.com"
                }
                ```"""
        self.assertIsNone(text_utils.extract_json(text))

    def test_extract_no_json_object(self):
        """Test case for text with no json object"""
        text = """This is a sample text with no json object."""
        self.assertIsNone(text_utils.extract_json(text))

    def test_extract_json_empty(self):
        """Test case for empty json object"""
        text = """test for empty json
                ```json
                {}
                ```"""
        result = text_utils.extract_json(text)
        self.assertEqual(result, {})

    def test_extract_with_multiple_json_objects(self):
        """Test case for text with multiple json objects"""
        text = """This is a sample text.
                ```json
                {
                    "name": "John Doe",
                    "email": "johndoe@example.com"
                }
                ```
                This is another json object.
                ```json
                {
                    "name": "Jane Doe",
                    "email": "janedoe@example.com"
                }
                ```"""
        expected = {
            "name": "John Doe",
            "email": "johndoe@example.com",
        }
        result = text_utils.extract_json(text)
        self.assertEqual(result, expected)


class TestUtilsExtractPythonCode(unittest.TestCase):
    def test_extract_python_code(self):
        input1 = "Here is some Python code:\n```python\nprint('Hello, World!')\n```"
        self.assertEqual(text_utils.extract_python_code(input1), "print('Hello, World!')")

        input2 = "Here is some text without Python code: print('Hello, World!')"
        self.assertIsNone(text_utils.extract_python_code(input2))

        input3 = "Multiple python code blocks \n```python\nprint('Block 1')\n```\n```python\nprint('Block 2')\n```"
        self.assertEqual(text_utils.extract_python_code(input3), "print('Block 1')")

        input4 = "Python code without 'python' after backticks \n```\na = 5\nb = 10\nprint(a+b)\n```"
        self.assertEqual(text_utils.extract_python_code(input4), "a = 5\nb = 10\nprint(a+b)")

        input5 = ""
        self.assertIsNone(text_utils.extract_python_code(input5))


if __name__ == "__main__":
    unittest.main()
