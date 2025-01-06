import re

from src.textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    result = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT or delimiter == "":
            result.append(node)
            continue

        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise Exception("Invalid Markdown: Missing closing delimiter")

        for i, text in enumerate(split_text):
            if text == "":
                continue
            if i % 2 == 0:
                result.append(TextNode(text, TextType.TEXT))
            else:
                result.append(TextNode(text, text_type))

    return result


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    alt_text: list[str] = re.findall(r"!\[(.*?)\]", text)
    url: list[str] = re.findall(r"\((.*?)\)", text)

    return list(zip(alt_text, url))


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    anchor_text: list[str] = re.findall(r"\[(.*?)\]", text)
    url: list[str] = re.findall(r"\((.*?)\)", text)

    return list(zip(anchor_text, url))


def split_nodes_image(old_nodes: list[TextNode]) -> list:
    result = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        text = node.text
        image_tuples = extract_markdown_images(text)

        if len(image_tuples) == 0:
            result.append(node)
        else:
            for image_alt, image_url in image_tuples:
                sections = text.split(f"![{image_alt}]({image_url})")
                if len(sections) != 2:
                    raise Exception("Invalid Markdown: image section not closed")

                if sections[0] != "":
                    result.append(TextNode(sections[0], TextType.TEXT))
                result.append(TextNode(image_alt, TextType.IMAGE, image_url))
                text = sections[1]

            if text != "":
                result.append(TextNode(text, TextType.TEXT))

    return result


def split_nodes_link(old_nodes: list[TextNode]):
    result = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        text = node.text
        link_tuples = extract_markdown_links(text)

        if len(link_tuples) == 0:
            result.append(node)
        else:
            for link_text, link_url in link_tuples:
                sections = text.split(f"[{link_text}]({link_url})")
                if len(sections) != 2:
                    raise Exception("Invalid Markdown: link section not closed")

                if sections[0] != "":
                    result.append(TextNode(sections[0], TextType.TEXT))
                result.append(TextNode(link_text, TextType.LINK, link_url))
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
