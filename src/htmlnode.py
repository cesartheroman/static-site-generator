from functools import reduce
from typing import List, Union


class HTMLNode:
    def __init__(
        self,
        tag: Union[str, None] = None,
        value: Union[str, None] = None,
        children: Union[List["HTMLNode"], None] = None,
        props: Union[dict[str, str], None] = None,
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


class LeafNode(HTMLNode):
    def __init__(self, tag: Union[str, None], value: str, props: Union[dict[str, str], None] = None):
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


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: List["HTMLNode"],
        props: Union[dict[str, str], None] = None,
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
