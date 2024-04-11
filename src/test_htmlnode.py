import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    """
    Test class for HTMLNode
    """

    def test_eq(self):
        """
        Make sure that props_to_html method works.
        """
        node = HTMLNode(
            "p",
            "this is a paragraph",
            [],
            {"href": "https://www.google.com", "target": "_blank"},
        )

        node2 = HTMLNode(
            "a",
            "this is an a tag",
            None,
            {"href": "https://www.google.com", "target": "_blank"},
        )

        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

        self.assertEqual(
            repr(node),
            "p, this is a paragraph, [], {'href': 'https://www.google.com', 'target': '_blank'}",
        )

        self.assertEqual(
            repr(node2),
            "a, this is an a tag, None, {'href': 'https://www.google.com', 'target': '_blank'}",
        )

    def test_to_html_no_children(self):
        """
        Test that to_html method works w/o children
        """
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        """
        Test that to_html method works w/o tag
        """
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_tags(self):
        """
        Test that to_html method works with tag and proper spacing
        """
        node = LeafNode(
            "a", "Click me!", {"href": "https://www.google.com", "target": "_blank"}
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com" target="_blank">Click me!</a>',
        )


if __name__ == "__main__":
    unittest.main()
