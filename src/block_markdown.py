def markdown_to_blocks(markdown: str) -> list[str]:
    """
    Should take raw markdown string (repping full doc) return list of block strings
    """
    split_md = markdown.split("\n\n")
    split_md = [block.strip() for block in split_md if block.strip()]

    return split_md
