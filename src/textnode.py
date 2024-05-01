from htmlnode import LeafNode

# Valid TextNode types
text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TextNode:
    """
    TextNode is an intermediate representation b/w Markdown and HTML, is specific
    to inline. The class will have the following:
    The text of the node
    The type of text this node contains like 'bold' 'italic'
    The URL of the link or image, if text is a link, default None
    """

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other_node):
        """
        Check to see if all properties of both TextNodes are equal
        """
        return (
            self.text == other_node.text
            and self.text_type == other_node.text_type
            and self.url == other_node.url
        )

    def __repr__(self):
        """
        Returns a string representation of the TextNode object
        """
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    def text_node_to_html_node(self, text_node):
        """
        Should handle each type of TextNode:
        text_type_text = 'text'
        etc...
        """
        if text_node.text_type == text_type_text:
            return LeafNode(None, text_node.text)
        if text_node.text_type == text_type_bold:
            return LeafNode("b", text_node.text)
        if text_node.text_type == text_type_italic:
            return LeafNode("i", text_node.text)
        if text_node.text_type == text_type_code:
            return LeafNode("code", text_node.text)
        if text_node.text_type == text_type_link:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        if text_node.text_type == text_type_image:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

        raise ValueError(f"Invalid text type: {text_node.text_type}")

    def split_nodes_delimiter(self, old_nodes, delimiter, text_type):
        """
        Takes a list of "old nodes", delimiter, and a text type.
        Return new list of nodes, where any "text" type nodes are (potentially)
        split into multiple nodes based on syntax

        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        Returns:
        [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text)
        ]
        """
        result = []

        for node in old_nodes:
            part1 = node.split(delimiter)
            result.append(part1)

        return result
