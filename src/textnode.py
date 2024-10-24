from enum import Enum
from typing import List, Union

from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(
        self, text: str, text_type: TextType, url: Union[str, None] = None
    ) -> None:
        self.text = text
        self.text_type = text_type.value
        self.url = url

    def __eq__(self, other) -> bool:
        if (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        ):
            return True
        return False

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT.value:
            return LeafNode(None, text_node.text)
        case TextType.BOLD.value:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC.value:
            return LeafNode("i", text_node.text)
        case TextType.CODE.value:
            return LeafNode("code", text_node.text)
        case TextType.LINK.value:
            return LeafNode("a", text_node.text, {"href": text_node.url or ""})

        case TextType.IMAGE.value:
            return LeafNode(
                "img", "", {"src": text_node.url or "", "alt": text_node.text or ""}
            )
        case _:
            raise Exception(f"Invalid TextType {text_node.text_type}")


def split_nodes_delimiter(
    old_nodes: List["TextNode"], delimiter: str, text_type: TextType
) -> List["TextNode"]:
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            result.append(node)
            continue

        words = node.text.split(delimiter)
        if len(words) % 2 == 0:
            raise Exception(
                f"Invalid Markdown syntax, missing closing delimiter '{delimiter}'"
            )

        pos = 0
        for word in words:
            if word == "":
                pos += 1
                continue
            if pos % 2 == 0:
                pos += 1
                result.append(TextNode(word, TextType.TEXT))
            else:
                pos += 1
                result.append(TextNode(word, text_type))

    return result
