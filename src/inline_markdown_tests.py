import unittest

from htmlnode import LeafNode
from inline_markdown import split_nodes_delimiter, text_node_to_html_node
from textnode import TextNode, TextType


class TestTextNodeConversion(unittest.TestCase):
    def test_TextNode_to_html_node(self):
        # Test conversion from text type to LeafNode
        node1 = TextNode("this is plain text", TextType.TEXT)
        leaf_node = text_node_to_html_node(node1)
        self.assertIsInstance(leaf_node, LeafNode)
        self.assertIsNone(leaf_node.tag)
        self.assertEqual(leaf_node.value, "this is plain text")
        self.assertIsNone(leaf_node.props)

        # Test conversion from bold to LeafNode
        node2 = TextNode("this is bold text", TextType.BOLD)
        leaf_node = text_node_to_html_node(node2)
        self.assertIsInstance(leaf_node, LeafNode)
        self.assertEqual(leaf_node.tag, "b")
        self.assertEqual(leaf_node.value, "this is bold text")
        self.assertIsNone(leaf_node.props)

        # Test conversion from italic to LeafNode
        node3 = TextNode("this is italic text", TextType.ITALIC)
        leaf_node = text_node_to_html_node(node3)
        self.assertIsInstance(leaf_node, LeafNode)
        self.assertEqual(leaf_node.tag, "i")
        self.assertEqual(leaf_node.value, "this is italic text")
        self.assertIsNone(leaf_node.props)

        # Test conversion from code to LeafNode
        node4 = TextNode("this is code text", TextType.CODE)
        leaf_node = text_node_to_html_node(node4)
        self.assertIsInstance(leaf_node, LeafNode)
        self.assertEqual(leaf_node.tag, "code")
        self.assertEqual(leaf_node.value, "this is code text")
        self.assertIsNone(leaf_node.props)

        # Test conversion from link to LeafNode
        node5 = TextNode("this is a link!", TextType.LINK, "http://example.com")
        leaf_node = text_node_to_html_node(node5)
        self.assertIsInstance(leaf_node, LeafNode)
        self.assertEqual(leaf_node.tag, "a")
        self.assertEqual(leaf_node.value, "this is a link!")
        self.assertEqual(leaf_node.props, {"href": "http://example.com"})

        # Test conversion from image to LeafNode
        node6 = TextNode("example image", TextType.IMAGE, "http://example.com")
        leaf_node = text_node_to_html_node(node6)
        self.assertIsInstance(leaf_node, LeafNode)
        self.assertEqual(leaf_node.tag, "img")
        self.assertEqual(leaf_node.value, "")
        self.assertEqual(
            leaf_node.props, {"src": "http://example.com", "alt": "example image"}
        )


class TestSplitNodeDelimiter(unittest.TestCase):
    def test_split_node_delimiter(self):
        # Test with bold text
        node1 = TextNode(
            "This is a text with a **bolded phrase** in the middle", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node1], "**", TextType.BOLD)
        expected = [
            TextNode("This is a text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
        ]
        self.assertEqual(
            new_nodes, expected, f"Expected: {expected} to be actual: {new_nodes}"
        )

        # Test with italic text
        node2 = TextNode(
            "This is a text with an *italic phrase* in the middle", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node2], "*", TextType.ITALIC)
        expected = [
            TextNode("This is a text with an ", TextType.TEXT),
            TextNode("italic phrase", TextType.ITALIC),
            TextNode(" in the middle", TextType.TEXT),
        ]
        self.assertEqual(
            new_nodes, expected, f"Expected: {expected} to be actual: {new_nodes}"
        )

        # Test with code text
        node3 = TextNode(
            "This is a text with a `code block` in the middle", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node3], "`", TextType.CODE)
        expected = [
            TextNode("This is a text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" in the middle", TextType.TEXT),
        ]
        self.assertEqual(
            new_nodes, expected, f"Expected: {expected} to be actual: {new_nodes}"
        )
