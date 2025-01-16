from functools import reduce


class HTMLNode:
    """
    Represents an HTML node with a tag, value, children, and properties.
    """

    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props is not None:
            return reduce(
                lambda acc, item: acc + f' {item[0]}="{item[1]}"',
                self.props.items(),
                "",
            )
        return ""

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class ParentNode(HTMLNode):
    """
    Represents a parent HTML node with a tag, children, and properties.
    """

    def __init__(
        self,
        tag: str,
        children: list[HTMLNode],
        props: dict[str, str] | None = None,
    ):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("Invalid ParentNode: must have a tag")

        if self.children is None or len(self.children) == 0:
            raise ValueError("Invalid ParentNode: must have children")

        result = ""
        for child in self.children:
            result += child.to_html()

        return f"<{self.tag}>{result}</{self.tag}>"

    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):
    """
    Represents a leaf HTML node with a tag, value, and properties.
    """

    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict[str, str] | None = None,
    ):
        super().__init__(
            tag,
            value,
            None,
            props,
        )

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("Invalid HTML: All leaf nodes must have a value")

        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
