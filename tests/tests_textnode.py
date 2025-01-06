import unittest

from src.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_TextNode_initialization(self):
        # Test basic initialization
        node = TextNode("Hello", TextType.TEXT)
        self.assertEqual(node.text, "Hello")
        self.assertEqual(node.text_type, TextType.TEXT)
        self.assertIsNone(node.url)

        # Test initialization w/URL
        node_with_url = TextNode("Click here", TextType.LINK, "https://example.com")
        self.assertEqual(node_with_url.text, "Click here")
        self.assertEqual(node_with_url.text_type, TextType.LINK)
        self.assertEqual(node_with_url.url, "https://example.com")

    def test_TextNode_equality(self):
        # Test equality between identical nodes
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

        # Test inequality with different text
        node3 = TextNode("Different", TextType.BOLD)
        self.assertNotEqual(node1, node3)

        # Test inequality w/diff type
        node4 = TextNode("This is a text node", TextType.IMAGE)
        self.assertNotEqual(node1, node4)

        # Test inequality w/diff URL
        node5 = TextNode("Click here", TextType.LINK, "https://example.com")
        node6 = TextNode("Click here", TextType.LINK, "https://different.com")
        self.assertNotEqual(node5, node6)

    def test_TextNode_str_representation(self):
        # Test __repr__ method
        node = TextNode("Testing repr", TextType.ITALIC)
        expected = f"TextNode(Testing repr, {TextType.ITALIC}, None)"
        self.assertEqual(repr(node), expected)

        node_with_url = TextNode("Link", TextType.LINK, "https://example.com")
        expected_with_url = f"TextNode(Link, {TextType.LINK}, https://example.com)"
        self.assertEqual(repr(node_with_url), expected_with_url)


if __name__ == "__main__":
    unittest.main()
