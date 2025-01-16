from src.htmlnode import LeafNode, ParentNode
from src.inline_markdown import text_to_textnodes
from src.textnode import text_node_to_html_node


def markdown_to_blocks(markdown: str) -> list[str]:
    """
    Should take raw markdown string (repping full doc) return list of block strings
    """
    split_md = markdown.split("\n\n")
    blocks = [stripped_block for block in split_md if (stripped_block := block.strip())]

    return blocks


def block_to_block_type(markdown_block: str) -> str:
    """
    Takes block of markdown and return string repping what type it is
    - heading
    - code
    - quote
    - unordered_list
    - ordered_list
    if none of previous conditions met, block is normal pragraph
    """
    lines = markdown_block.split("\n")
    if markdown_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return "heading"
    if markdown_block.startswith("```") and markdown_block.endswith("```"):
        return "code"
    if markdown_block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return "paragraph"
        return "quote"
    if markdown_block.startswith(("* ", "- ")):
        for line in lines:
            if not line.startswith(("* ", "- ")):
                return "paragraph"
        return "unordered_list"
    if markdown_block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return "paragraph"
            i += 1
        return "ordered_list"
    return "paragraph"


def markdown_to_html_node(markdown: str) -> ParentNode:
    """
    converts full md doc to a single parent HTMLNode with many child objects representing nested elements
    """
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == "paragraph":
            p_items = []
            lines = block.split("\n")
            paragraph = " ".join(lines)
            text_nodes = text_to_textnodes(paragraph)

            for text_node in text_nodes:
                html_node = text_node_to_html_node(text_node)
                p_items.append(html_node)

            children.append(ParentNode("p", p_items))

        if block_type == "unordered_list":
            li_items = []
            lines = block.split("\n")

            for line in lines:
                li_children = []
                text = line[2:]
                text_nodes = text_to_textnodes(text)

                for text_node in text_nodes:
                    html_node = text_node_to_html_node(text_node)
                    li_children.append(html_node)

                li_items.append(ParentNode("li", li_children))

            children.append(ParentNode("ul", li_items))

        if block_type == "ordered_list":
            li_items = []
            lines = block.split("\n")

            for line in lines:
                text = line[3:]
                text_nodes = text_to_textnodes(text)
                li_children = []

                for text_node in text_nodes:
                    html_node = text_node_to_html_node(text_node)
                    li_children.append(html_node)

                li_items.append(ParentNode("li", li_children))

            children.append(ParentNode("ol", li_items))

    # print("children:", children)
    return ParentNode("div", children)
