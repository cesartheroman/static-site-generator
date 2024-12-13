import unittest

from htmlnode import LeafNode
from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
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
        node = TextNode(
            "a picture of benji", TextType.IMAGE, "http://benjitheroman.com"
        )
        leaf_node = text_node_to_html_node(node)
        self._assert_common_leaf_node_properties(
            leaf_node,
            "img",
            "",
            {"src": "http://benjitheroman.com", "alt": "a picture of benji"},
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
        self.assertListEqual(
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
        self.assertListEqual(
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
        self.assertListEqual(
            new_nodes, expected, f"Expected: {expected} to be actual: {new_nodes}"
        )

    def test_split_node_delimiter_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(new_nodes, [])

    def test_split_node_delimiter_no_delimiter(self):
        node = TextNode("Plain text without delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "", TextType.BOLD)
        self.assertListEqual(new_nodes, [node])

    def test_split_node_delimiter_multi_occurence(self):
        node = TextNode("**bold** normal **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" normal ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertListEqual(new_nodes, expected)


class TestExtractMarkdownFromText(unittest.TestCase):
    def test_image_extraction(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        actual = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertListEqual(
            actual, expected, f"Expected: {expected}, to equal actual: {actual}"
        )

    def test_link_extraction(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        actual = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(
            actual, expected, f"Expected: {expected}, to equal actual: {actual}"
        )


class TestSplitNodes(unittest.TestCase):
    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) with some extra text",
            TextType.TEXT,
        )
        actual = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
            TextNode(" with some extra text", TextType.TEXT),
        ]
        self.assertListEqual(
            actual, expected, f"Expected: {expected}, to equal actual: {actual}"
        )

    def test_split_nodes_image(self):
        node = TextNode(
            "This is an image with benji smiling ![benji smile](https://www.benjitheroman.dev) and an image with benji barking ![benji bark](https://www.instagram.com/@benjitheroman) in the park",
            TextType.TEXT,
        )
        actual = split_nodes_image([node])
        expected = [
            TextNode("This is an image with benji smiling ", TextType.TEXT),
            TextNode("benji smile", TextType.IMAGE, "https://www.benjitheroman.dev"),
            TextNode(" and an image with benji barking ", TextType.TEXT),
            TextNode(
                "benji bark", TextType.IMAGE, "https://www.instagram.com/@benjitheroman"
            ),
            TextNode(" in the park", TextType.TEXT),
        ]
        self.assertListEqual(
            actual, expected, f"Expected: {expected}, to equal actual: {actual}"
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_basic_init(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        actual = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(
            actual, expected, f"Expected: {expected}, to equal actual: {actual}"
        )


if __name__ == "__main__":
    unittest.main()
