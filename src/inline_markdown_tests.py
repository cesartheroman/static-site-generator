import unittest

from htmlnode import LeafNode
from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNodeConversion(unittest.TestCase):
    """Test suite for text_node_to_html_node function.

    Tests the conversion of various TextNode types to their corresponding
    HTML LeafNode representations.
    """

    def _assert_common_leaf_node_properties(
        self,
        leaf_node: LeafNode,
        expected_tag: str | None,
        expected_value: str,
        expected_props: dict[str, str] | None = None,
    ):
        self.assertIsInstance(leaf_node, LeafNode)
        self.assertEqual(leaf_node.tag, expected_tag)
        self.assertEqual(leaf_node.value, expected_value)
        self.assertEqual(leaf_node.props, expected_props)

    def test_plain_text_conversion(self):
        node = TextNode("this is plain text", TextType.TEXT)
        leaf_node = text_node_to_html_node(node)
        self._assert_common_leaf_node_properties(leaf_node, None, "this is plain text")

    def test_bold_text_conversion(self):
        node = TextNode("this is bold text", TextType.BOLD)
        leaf_node = text_node_to_html_node(node)
        self._assert_common_leaf_node_properties(leaf_node, "b", "this is bold text")

    def test_italic_text_conversion(self):
        node = TextNode("this is italic text", TextType.ITALIC)
        leaf_node = text_node_to_html_node(node)
        self._assert_common_leaf_node_properties(leaf_node, "i", "this is italic text")

    def test_code_text_conversion(self):
        node = TextNode("this is code text", TextType.CODE)
        leaf_node = text_node_to_html_node(node)
        self._assert_common_leaf_node_properties(leaf_node, "code", "this is code text")

    def test_link_text_conversion(self):
        node = TextNode("this is a link!", TextType.LINK, "http://cesartheroman.com")
        leaf_node = text_node_to_html_node(node)
        self._assert_common_leaf_node_properties(
            leaf_node, "a", "this is a link!", {"href": "http://cesartheroman.com"}
        )

    def test_image_text_conversion(self):
        node = TextNode("a picture of benji", TextType.IMAGE, "http://benjitheroman.com")
        leaf_node = text_node_to_html_node(node)
        self._assert_common_leaf_node_properties(
            leaf_node, "img", "", {"src": "http://benjitheroman.com", "alt": "a picture of benji"}
        )


class TestSplitNodeDelimiter(unittest.TestCase):
    """Test suite for split_nodes_delimiter function.

    Tests the parsing of markdown-style text nodes with different delimiters
    and ensures correct node splitting and type assignment.
    """

    def test_split_node_delimiter_bold(self):
        node = TextNode(
            "This is a text with a **bolded phrase** in the middle", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is a text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
        ]
        self.assertEqual(
            new_nodes, expected, f"Expected: {expected} to be actual: {new_nodes}"
        )

    def test_split_node_delimiter_italic(self):
        node = TextNode(
            "This is a text with an *italic phrase* in the middle", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("This is a text with an ", TextType.TEXT),
            TextNode("italic phrase", TextType.ITALIC),
            TextNode(" in the middle", TextType.TEXT),
        ]
        self.assertEqual(
            new_nodes, expected, f"Expected: {expected} to be actual: {new_nodes}"
        )

    def test_split_node_delimiter_code(self):
        node = TextNode(
            "This is a text with a `code block` in the middle", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is a text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" in the middle", TextType.TEXT),
        ]
        self.assertEqual(
            new_nodes, expected, f"Expected: {expected} to be actual: {new_nodes}"
        )

    def test_split_node_delimiter_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [])

    def test_split_node_delimiter_no_delimiter(self):
        node = TextNode("Plain text without delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "", TextType.BOLD)
        self.assertEqual(new_nodes, [node])

    def test_split_node_delimiter_multi_occurence(self):
        node = TextNode("**bold** normal **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" normal ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)


# class TestExtractMarkdownImages(unittest.TestCase):
#     def

if __name__ == "__main__":
    unittest.main()
