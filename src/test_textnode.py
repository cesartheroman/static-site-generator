import unittest

from textnode import (
    TextNode,
    text_type_bold,
    text_type_code,
    text_type_italic,
    text_type_text,
)


class TestTextNode(unittest.TestCase):
    """
    TestTextNode will construct text nodes for testing purposes
    """

    def test_eq(self):
        """
        This test creates two TextNode objects with the same properties and
        asserts that they're equal.
        """
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
