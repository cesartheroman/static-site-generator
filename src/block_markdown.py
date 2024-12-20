from htmlnode import HTMLNode


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


def markdown_to_html_nodes(markdown: str) -> HTMLNode:
    "converts full md doc to a single parent HTMLNode with many child objects repping nested elements"
    print(markdown)
    return HTMLNode()
