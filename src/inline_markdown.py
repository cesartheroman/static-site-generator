from typing import List

from htmlnode import LeafNode
from textnode import TextNode, TextType


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

        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception(
                f"Invalid Markdown: missing closing delimiter '{delimiter}'"
            )

        for i, part in enumerate(parts):
            if i % 2 == 0:
                result.append(TextNode(part, TextType.TEXT))
            else:
                result.append(TextNode(part, text_type))

    return result

# def extract_markdown_images(text: str)-> List[tuple[str,str]]:
#     print(text)
