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


class ParentNode(HTMLNode):
    """
    Handles the nesting of HTML nodes inside of one another.
    Any HTML node that is not a leaf is a parent node.
    """

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        """
        If no tag, raises a ValueError
        If no children, raise ValueError with differnt message
        Should return a string representing HTML tag of node and its children, should be recursive
        with each recursion using a new node instance.
        eg:
        node = ParentNode("p", [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode('i', "italic text"),
        LeafNode(None, "Normal text"),
        ])
        node.to_html()
        should return:
        <p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>
        """
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")

        if not self.children:
            raise ValueError("Invalid HTML: no children")

        html = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            if hasattr(child, "to_html"):
                html += child.to_html()
            else:
                html += child

        html += f"</{self.tag}>"
        return html

        # official solution:
        # children_html = ""
        # for child in self.children:
        #     children_html += child.to_html()
        # return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
