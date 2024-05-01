import unittest

from textnode import TextNode


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

    def test_split_nodes_delimiter(self):
        """
        This test checks to see if a TextNode is successfully split by delimiter
        """
        old_node = TextNode("This is text with a `code block` word", "text")
        new_nodes = old_node.split_nodes_delimiter([old_node], "`", "code")

        text_type_text = "text"
        text_type_code = "code"

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


if __name__ == "__main__":
    unittest.main()
