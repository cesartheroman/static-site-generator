import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(
            "p",
            "this is a paragraph",
            None,
            {"href": "https://www.google.com", "target": "_blank"},
        )
        # node2 = HTMLNode("h1", "this is an h1", None, {"target": "_blank"})
        self.assertEqual(node.props_to_html(), 'href="https://www.google.com"')


if __name__ == "__main__":
    unittest.main()
