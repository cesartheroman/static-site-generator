from enum import Enum

from src.htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
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
    text_type = text_node.text_type

    if text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)

    if text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)

    if text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)

    if text_type == TextType.CODE:
        return LeafNode("code", text_node.text)

    if text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url or ""})

    if text_type == TextType.IMAGE:
        return LeafNode(
            "img", "", {"src": text_node.url or "", "alt": text_node.text or ""}
        )

    raise Exception(f"Invalid TextType {text_type}")
