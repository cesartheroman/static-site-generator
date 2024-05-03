from textnode import (
    TextNode,
    text_type_bold,
    text_type_code,
    text_type_italic,
    text_type_text,
)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Takes a list of "old nodes", delimiter, and a text type.
    Return new list of nodes, where any "text" type nodes are (potentially)
    split into multiple nodes based on syntax

    node = TextNode("This is text with a `code block` word", text_type_text)
    new_nodes = split_nodes_delimiter([node], "`", text_type_code)
    Returns:
    [
        TextNode("This is text with a ", text_type_text),
        TextNode("code block", text_type_code),
        TextNode(" word", text_type_text)
    ]
    """
    result = []

    for node in old_nodes:
        if node.text_type == "text":
            split_text = node.text.split(delimiter)
            if len(split_text) == 2:
                raise Exception("Missing closing delimiter for node")

            for i, chunk in enumerate(split_text):
                if chunk == "":
                    continue

                if i % 2 == 0:
                    result.append(TextNode(chunk, node.text_type))
                else:
                    result.append(TextNode(chunk, text_type))
        else:
            result.append(node)

    return result
