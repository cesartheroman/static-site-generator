from functools import reduce
from typing import List, Union


class HTMLNode:
    def __init__(
        self,
        tag: Union[str, None] = None,
        children: Union[List["HTMLNode"], None] = None,
        props: Union[dict[str, str], None] = None,
    ):
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self) -> None:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props is not None:
            return reduce(
                lambda acc, item: acc + f' {item[0]}="{item[1]}"',
                self.props.items(),
                "",
            )
        return ""

    def __eq__(self, other) -> bool:
        if (
            self.tag == other.tag
            and self.children == other.children
            and self.props == other.props
        ):
            return True
        return False

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.children}, {self.props})"
