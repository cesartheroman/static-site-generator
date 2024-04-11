class HTMLNode:
    """
    HTMLNode class will represent a 'node' in an HTML doc tree like <p> tag
    and its contents, or <a> and its contents. Purpose is to render itself as HTML.

    HTMLNode class will have 4 data members:
    1. tag - string representation of HTML tag name eg. 'p' 'a', 'h1', etc
    2. value - string representation the value of the HTML tag(eg. text in paragraph)
    3. children - list of HTMLNode objects repping children of this node
    4. props - dictionary of key-value pairs repping HTML tag attributes.
    (eg. link tag <a> might have {'href': 'https://www.google.com'})
    """

    def __init__(self, tag=None, value=None, children=None, props=None):
        """
        Every data member should be optional and default to None
        - HTMLNode w/o tag will render as raw text
        - HTMLNode w/o value will be assumed to have children
        - HTMLNode w/o children will be assumed to have a value
        - HTMLNode w/o props won't have any attributes
        """
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """
        For now just raise a NotImplementedError
        """
        raise NotImplementedError()

    def props_to_html(self):
        """
        Should return a string representation of the HTML attributes of the node.

        if self.props is
        {"href": "https://www.google.com", "target": "_blank"}

        then self.props_to_html(self) should return:
        href="https://www.google.com" target="_blank"
        """
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'

        return props_html

    def __repr__(self):
        """
        Way to print an HTMLNode object and see tag, value, children, and props
        """
        return f"{self.tag}, {self.value}, {self.children}, {self.props}"


class LeafNode(HTMLNode):
    """
    The LeafNode is a type of HTMLNode that represents a single HTML tag with no
    children.
    Eg:
    <p>This is a paragraph of text.</p>
    """

    def __init__(self, tag, value, props=None):
        """
        Value data member should be required
        Should not allow for children
        """
        super().__init__(tag, value, None, props)

    def to_html(self):
        """
        Should render a leaf node as an HTML string by returning a string.
        If no value, raise ValueError. All leaf nodes require a value
        If no tag, value should be returned as raw text
        Otherwise, render an HTML tag, eg:

        LeafNode("p", "This is a paragraph of text.")
        LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        Should render as:
        <p>This is a paragraph of text.</p>
        <a href='https://www.google.com'>Click me!</a>
        """
        if self.value is None:
            raise ValueError

        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
