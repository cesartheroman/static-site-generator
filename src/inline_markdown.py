import re

from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
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


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    alt_text: list[str] = re.findall(r"!\[(.*?)\]", text)
    url: list[str] = re.findall(r"\((.*?)\)", text)

    return list(zip(alt_text, url))


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    anchor_text = re.findall(r"\[(.*?)\]", text)
    url = re.findall(r"\((.*?)\)", text)

    return list(zip(anchor_text, url))


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    result: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            result.append(node)
            continue

        text = node.text
        image_tuples = extract_markdown_images(text)
        if len(image_tuples) == 0:
            result.append(node)
        else:
            for image in image_tuples:
                image_alt, image_link = image
                sections = text.split(f"![{image_alt}]({image_link})", 1)

                if len(sections) != 2:
                    raise Exception("Invalid Markdown: image section not closed")
                if sections[0] != "":
                    result.append(TextNode(sections[0], TextType.TEXT))
                result.append(TextNode(image_alt, TextType.IMAGE, image_link))
                text = sections[1]

            if text != "":
                result.append(TextNode(text, TextType.TEXT))

    return result


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    result: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            result.append(node)
            continue

        text = node.text
        link_tuples = extract_markdown_links(text)
        if len(link_tuples) == 0:
            result.append(node)
        else:
            for link in link_tuples:
                anchor_text, url = link
                sections = text.split(f"[{anchor_text}]({url})")

                if len(sections) != 2:
                    raise ValueError("Invalid Markdown: link section not closed")
                if sections[0] != "":
                    result.append(TextNode(sections[0], TextType.TEXT))
                result.append(TextNode(anchor_text, TextType.LINK, url))
                text = sections[1]

            if text != "":
                result.append(TextNode(text, TextType.TEXT))

    return result


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes
