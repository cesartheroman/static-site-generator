from src.htmlnode import HTMLNode


def markdown_to_blocks(markdown: str) -> list[str]:
    """
    Should take raw markdown string (repping full doc) return list of block strings
    """
    split_md = markdown.split("\n\n")
    blocks = [block.strip() for block in split_md if block.strip()]

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


def markdown_to_html_nodes(markdown: str):
    """
    converts full md doc to a single parent HTMLNode with many child objects representing nested elements
    - Split markdown into blocks (leverage previous function)
    - Loop over each block
        - Determine type of block (leverage prev function)
        - Based on type of block, create new HTMLNode with proper data
        - Assign proper child HTMLNode objects to the block node. Created a shared text_to_children(text) function that
        works for all block types. Takes string of text and returns list of HTMLNodes that represent inline markdown using previously created functions (think TextNode -> HTMLNode)
    - Make all block nodes children under a single parent HTML node (should just be a div) and return
    """
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == "paragraphs":
            children.append(HTMLNode("p", block))

    return HTMLNode("div", None, children=children)
