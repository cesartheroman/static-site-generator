import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
        self.assertIsNotNone(node1.children)
        self.assertEqual(len(node1.children or []), 2)
        self.assertTrue(all(isinstance(x, HTMLNode) for x in node1.children or []))
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

    def test_HTMLNode_str_representation(self):
        # Test __repr__ method w/same content
        node1 = HTMLNode(
            "p", None, [HTMLNode("img"), HTMLNode("div")], {"class": "container"}
        )
        node2 = HTMLNode(
            "p", None, [HTMLNode("img"), HTMLNode("div")], {"class": "container"}
        )
        self.assertEqual(
            repr(node1), repr(node2), "Nodes should have same str representation"
        )

        # Test __repr__ method w/o same content
        node3 = HTMLNode(
            "p", None, [HTMLNode("h1"), HTMLNode("div")], {"class": "container"}
        )
        self.assertNotEqual(
            repr(node1), repr(node3), "Nodes str representation not should not be equal"
        )


class TestLeafNode(unittest.TestCase):
    def test_LeafNode_initialization(self):
        # Test basic init
        node1 = LeafNode("div", "This is a div!")
        self.assertEqual(node1.tag, "div")
        self.assertEqual(node1.value, "This is a div!")
        self.assertIsNone(node1.children)

        # Test init with props
        node2 = LeafNode("p", "hey there", {"class": "text-bold", "id": "greeting"})
        self.assertEqual(node2.tag, "p")
        self.assertEqual(node2.value, "hey there")
        self.assertIsNone(node2.children)
        self.assertEqual(node2.props, {"class": "text-bold", "id": "greeting"})

        # Test init with None tag
        node3 = LeafNode(None, "Just text")
        self.assertIsNone(node3.tag)
        self.assertEqual(node3.value, "Just text")
        self.assertIsNone(node3.children)

    def test_LeafNode_to_html(self):
        # Test cases with valid tag and value
        node1 = LeafNode("p", "This is a paragraph of text.")
        actual = node1.to_html()
        expected = "<p>This is a paragraph of text.</p>"
        self.assertEqual(
            actual, expected, f"Expected {expected}, to be equal to {actual}"
        )

        # Test cases with valid tag, value, and props
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        actual = node2.to_html()
        expected = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(
            actual, expected, f"Expected: {expected}, to be equal to actual: {actual}"
        )

        # Test case where no tag (return text)
        node3 = LeafNode(None, "Just text")
        actual = node3.to_html()
        expected = "Just text"
        self.assertEqual(
            actual, expected, f"Expected: {expected}, to be equal to actual: {actual}"
        )

        # Test invalid case where no value
        node4 = LeafNode("p", None)  # type: ignore
        with self.assertRaises(ValueError) as context:
            node4.to_html()
        self.assertEqual(
            str(context.exception), "Invalid HTML: All leaf nodes must have a value"
        )

    def test_LeafNode_str_representation(self):
        # Test __repr__ method
        node1 = LeafNode("p", "this is a paragraph", {"class": "container"})
        actual = repr(node1)
        expected = "LeafNode(p, this is a paragraph, {'class': 'container'})"
        self.assertEqual(
            actual, expected, f"Expected: {expected}, to be equal to actual: {actual}"
        )


class TestParentNode(unittest.TestCase):
    def test_ParentNode_initialization(self):
        # Test basic init
        node1 = ParentNode(
            "div",
            [
                LeafNode("b", "bold text"),
                LeafNode("p", "this is a paragraph"),
            ],
        )
        self.assertIsInstance(node1, ParentNode)
        self.assertEqual(len(node1.children or []), 2)
        self.assertTrue(all(isinstance(x, LeafNode) for x in node1.children or []))

    def test_ParentNode_to_html(self):
        # Test to_html with valid arguments
        node1 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        actual = node1.to_html()
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(
            actual, expected, f"Expected: {expected}, to be equal to actual: {actual}"
        )

        # Test invalid case with no tag
        node2 = ParentNode(None, [LeafNode("span", "this is a span")])  # type: ignore
        with self.assertRaises(ValueError) as context:
            node2.to_html()
        self.assertEqual(
            str(context.exception),
            "Invalid ParentNode: must have a tag",
        )

        # Test invalid case with no children
        node3 = ParentNode("i", None)  # type: ignore
        with self.assertRaises(ValueError) as context:
            node3.to_html()
        self.assertEqual(
            str(context.exception), "Invalid ParentNode: must have children"
        )

        # Test with empty children
        node3 = ParentNode("i", [])
        with self.assertRaises(ValueError) as context:
            node3.to_html()
        self.assertEqual(
            str(context.exception), "Invalid ParentNode: must have children"
        )

        # Test with nested ParentNodes and LeafNodes
        node4 = ParentNode(
            "p",
            [
                ParentNode(
                    "b",
                    [ParentNode("i", [LeafNode("a", "this is an a tag")])],
                ),
                LeafNode("h1", "this is an h1 tag"),
            ],
        )
        actual = node4.to_html()
        expected = (
            "<p><b><i><a>this is an a tag</a></i></b><h1>this is an h1 tag</h1></p>"
        )
        self.assertEqual(
            actual, expected, f"Expected: {expected}, to be equal to actual: {actual}"
        )

    def test_ParentNode_str_representation(self):
        # Test __repr__ method
        node1 = ParentNode(
            "p",
            [
                LeafNode("b", "bold text"),
                LeafNode("p", "this is a paragraph"),
            ],
            {"class": "container"},
        )
        actual = repr(node1)
        expected = "ParentNode(p, children: [LeafNode(b, bold text, None), LeafNode(p, this is a paragraph, None)], {'class': 'container'})"
        self.assertEqual(
            actual, expected, f"Expected: {expected}, to be equal to actual: {actual}"
        )


if __name__ == "__main__":
    unittest.main()
