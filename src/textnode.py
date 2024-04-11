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
