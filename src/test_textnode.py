import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_initialization(self):
        """Test basic initialization of TextNode"""
        # Test basic initialization
        node = TextNode("Hello", TextType.TEXT)
        self.assertEqual(node.text, "Hello")
        self.assertEqual(node.text_type, "text")
        self.assertIsNone(node.url)

        # Test initialization w/URL
        node_with_url = TextNode("Click here", TextType.LINKS, "https://example.com")
        self.assertEqual(node_with_url.text, "Click here")
        self.assertEqual(node_with_url.text_type, "links")
        self.assertEqual(node_with_url.url, "https://example.com")

    def test_equality(self):
        """Test equality comparison between TextNodes"""
        # Test equality between identical nodes
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

        # Test inequality with different text
        node3 = TextNode("Different", TextType.BOLD)
        self.assertNotEqual(node1, node3)

        # Test inequality w/diff type
        node4 = TextNode("This is a text node", TextType.IMAGES)
        self.assertNotEqual(node1, node4)

        # Test inequality w/diff URL
        node5 = TextNode("Click here", TextType.LINKS, "https://example.com")
        node6 = TextNode("Click here", TextType.LINKS, "https://different.com")
        self.assertNotEqual(node5, node6)

    def test_str_representation(self):
        """Test string representation of TextNode"""
        # Test __repr__ method
        node = TextNode("Testing repr", TextType.ITALIC)
        expected = "TextNode(Testing repr, italic, None)"
        self.assertEqual(repr(node), expected)

        node_with_url = TextNode("Link", TextType.LINKS, "https://example.com")
        expected_with_url = "TextNode(Link, links, https://example.com)"
        self.assertEqual(repr(node_with_url), expected_with_url)


if __name__ == "__main__":
    unittest.main()
