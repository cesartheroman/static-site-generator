import unittest

from htmlnode import HTMLNode


class TextHTMLNode(unittest.TestCase):
    def test_HTMLNode_initialization(self):
        # Test empty init
        node = HTMLNode()
        self.assertIsInstance(node, HTMLNode)
        self.assertIsNone(node.tag, "Expected tag to be None by default")
        self.assertIsNone(node.children, "Expected children to be None by default")
        self.assertIsNone(node.props, "Expected props to be None by default")

        # Test basic init
        node1 = HTMLNode(
            tag="p",
            children=[HTMLNode(tag="p"), HTMLNode(tag="span")],
            props={"class": "container"},
        )
        self.assertEqual(node1.tag, "p")
        self.assertEqual(len(node1.children), 2)
        self.assertTrue(all(isinstance(x, HTMLNode) for x in node1.children))
        self.assertEqual(node1.props, {"class": "container"})

    def test_HTMLNode_props_to_html(self):
        # Test valid input to props_to_html
        node1 = HTMLNode(
            tag="div",
            children=[HTMLNode(tag="p")],
            props={"href": "https://www.google.com", "target": "_blank"},
        )
        actual = node1.props_to_html()
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(actual, expected, f"Expected: {expected}, Got: {actual}")

        # Test if props is None
        node2 = HTMLNode(tag="a", children=None, props=None)
        actual = node2.props_to_html()
        expected = ""
        self.assertEqual(actual, expected, "Expected props to be empty string")

    def test_HTMLNode_equality(self):
        # Test equal nodes
        node1 = HTMLNode(
            tag="a",
            children=[HTMLNode("h1"), HTMLNode("h2")],
            props={"class": "greeting", "href": "https://boot.dev"},
        )
        node2 = HTMLNode(
            tag="a",
            children=[HTMLNode("h1"), HTMLNode("h2")],
            props={"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(node1, node2, "Nodes should be equal")

        # Test unequal nodes
        node3 = HTMLNode(tag="a", children=[HTMLNode("h2")], props=None)
        self.assertNotEqual(node1, node3, "Nodes should not be equal")

    def test_HTMLNode_str_representation(self):
        # Test __repr__ method w/same content
        node1 = HTMLNode(
            "p", [HTMLNode("img"), HTMLNode("div")], {"class": "container"}
        )
        node2 = HTMLNode(
            "p", [HTMLNode("img"), HTMLNode("div")], {"class": "container"}
        )

        self.assertEqual(
            repr(node1), repr(node2), "Nodes should have same str representation"
        )

        # Test __repr__ method w/o same content
        node3 = HTMLNode("p", [HTMLNode("h1"), HTMLNode("div")], {"class": "container"})
        self.assertNotEqual(
            repr(node1), repr(node3), "Nodes str representation not should not be equal"
        )


if __name__ == "__main__":
    unittest.main()
