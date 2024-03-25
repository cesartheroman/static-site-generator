import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
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
            node.props_to_html(), 'href="https://www.google.com" target="_blank"'
        )

        self.assertEqual(
            repr(node),
            "p, this is a paragraph, [], {'href': 'https://www.google.com', 'target': '_blank'}",
        )

        self.assertEqual(
            repr(node2),
            "a, this is an a tag, None, {'href': 'https://www.google.com', 'target': '_blank'}",
        )


if __name__ == "__main__":
    unittest.main()
