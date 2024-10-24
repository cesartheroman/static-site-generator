import re
from typing import List

from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: List["TextNode"], delimiter: str, text_type: TextType
) -> List["TextNode"]:
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value or delimiter == "":
            result.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception(
                f"Invalid Markdown: missing closing delimiter '{delimiter}'"
            )

        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                result.append(TextNode(part, TextType.TEXT))
            else:
                result.append(TextNode(part, text_type))

    return result


def extract_markdown_images(text: str) -> List[tuple[str, str]]:
    alt_text: List[str] = re.findall(r"\[(.*?)\]", text)
    url: List[str] = re.findall(r"\((.*?)\)", text)

    return list(zip(alt_text, url))


def extract_markdown_links(text: str) -> List[tuple[str, str]]:
    anchor_text = re.findall(r"\[(.*?)\]", text)
    url = re.findall(r"\((.*?)\)", text)

    return list(zip(anchor_text, url))
