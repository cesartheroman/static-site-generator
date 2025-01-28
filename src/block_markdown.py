from .htmlnode import LeafNode, ParentNode
from .inline_markdown import text_to_textnodes
from .textnode import text_node_to_html_node


def markdown_to_blocks(markdown: str) -> list[str]:
    """
    Takes raw markdown string and converts it to blocks using newlines as delimiter.
    """
    split_md = markdown.split("\n\n")
    blocks = [stripped_block for block in split_md if (stripped_block := block.strip())]

    return blocks


def block_to_block_type(markdown_block: str) -> str:
    """
    Takes markdown block and returns string representation of type
    Defaults to paragraph type if none other found
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
    Converts full md doc to a single parent HTMLNode with many child objects representing nested elements
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

        if block_type == "heading":
            lines = block.split("\n")
            for line in lines:
                i = 0
                while line[i] == "#":
                    i += 1
                text = line[i + 1 :].strip()
                text_nodes = text_to_textnodes(text)
                heading_children = []

                for text_node in text_nodes:
                    html_node = text_node_to_html_node(text_node)
                    heading_children.append(html_node)

                children.append(ParentNode(f"h{i}", heading_children))


        if block_type == "quote":
            lines = block.split("\n")
            new_lines = []

            for line in lines:
                new_lines.append(line[1:].strip())

            text = " ".join(new_lines)
            text_nodes = text_to_textnodes(text)
            q_children = []

            for text_node in text_nodes:
                html_node = text_node_to_html_node(text_node)
                q_children.append(html_node)

            children.append(ParentNode("blockquote", q_children))

        if block_type == "code":
            if not block.startswith("```") or not block.endswith("```"):
                raise ValueError("Missing starting or closing delimiters")

            code_items = []
            html_nodes = []

            text = block[4:-3]
            text_nodes = text_to_textnodes(text)

            for text_node in text_nodes:
                html_node = text_node_to_html_node(text_node)
                html_nodes.append(html_node)

            code_items.append(ParentNode("code", html_nodes))

            children.append(ParentNode("pre", code_items))

    return ParentNode("div", children)
