import unittest

from inline_markdown import split_nodes_delimiter
from textnode import (
    TextNode,
    text_type_bold,
    text_type_code,
    text_type_italic,
    text_type_text,
)


class TestInlineMarkdown(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        """
        This test checks to see if a TextNode is successfully split by delimiter
        """
        old_node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([old_node], "`", text_type_code)

        expected_result = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ]

        self.assertEqual(
            new_nodes,
            expected_result,
            f"Expected: {expected_result}\nActual: {new_nodes}",
        )

    def test_split_delimiter_empty_string(self):
        """
        This test checks to see if split_text includes empty strings, esp at beginning or end of array
        """
        old_node = TextNode("`code1`text`code2``code3`text`code4`", text_type_text)
        new_nodes = split_nodes_delimiter([old_node], "`", text_type_code)

        expected_result = [
            TextNode("code1", text_type_code),
            TextNode("text", text_type_text),
            TextNode("code2", text_type_code),
            TextNode("code3", text_type_code),
            TextNode("text", text_type_text),
            TextNode("code4", text_type_code),
        ]
        self.assertEqual(
            new_nodes,
            expected_result,
            f"Expected: {expected_result}\nActual: {new_nodes}",
        )

    def test_split_delimeter_invalid_markdown(self):
        """
        This test checks to see that if a closing delimiter is not present, we should respond with an error message.
        """
        old_node = TextNode("this is a `code node gone wrong", text_type_text)

        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([old_node], "`", text_type_code)

        self.assertTrue("Missing closing delimiter for node" in str(context.exception))

    # def test_split_delimiter_various(self):
    # TODO: finish implementing the three delimiters
