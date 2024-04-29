import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_parent_node(self):
        """
        Basic nesting with leafnodes of a simple nested structure
        """
        node = ParentNode(
            "a",
            [
                LeafNode("div", "this is a div"),
                LeafNode("p", "this is a paragraph"),
            ],
        )
        self.assertEqual(
            node.to_html(), "<a><div>this is a div</div><p>this is a paragraph</p></a>"
        )

    def test_deeply_nested(self):
        """
        Testing a deeply nested structure with multiple levels of ParentNode and LeafNode
        """
        inner_node = ParentNode("div", [LeafNode("span", "deeply nested span")])
        mid_node = ParentNode(
            "section", [LeafNode("p", "nested paragraph"), inner_node]
        )
        outer_node = ParentNode("article", [LeafNode("h1", "header"), mid_node])
        self.assertEqual(
            outer_node.to_html(),
            "<article><h1>header</h1><section><p>nested paragraph</p><div><span>deeply nested span</span></div></section></article>",
        )

    def test_mixed_properties(self):
        """
        Testing nodes that have properies set, and also testing a mix of Node types
        """
        complex_node = ParentNode(
            "div",
            [
                LeafNode(
                    "a",
                    "click here",
                    {"href": "https://www.example.com", "target": "_blank"},
                ),
                "raw text",
                ParentNode("footer", [LeafNode("b", "bold text"), " more raw text"]),
            ],
            {"id": "container", "class": "my-container"},
        )
        self.assertEqual(
            complex_node.to_html(),
            '<div id="container" class="my-container"><a href="https://www.example.com" target="_blank">click here</a>raw text<footer><b>bold text</b> more raw text</footer></div>',
        )


if __name__ == "__main__":
    unittest.main()
