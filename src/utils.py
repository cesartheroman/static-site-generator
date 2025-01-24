"""
Create an extract_title(markdown) function.
It should pull the h1 header from the markdown file (the line that starts with a single #) and return it.
If there is no h1 header, raise an exception.
extract_title("# Hello") should return "Hello" (strip the # and any leading or trailing whitespace)
"""

from src.block_markdown import markdown_to_blocks


def extract_title(markdown: str):
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        if block.startswith("#") and len(block) > 1 and block[1] == " ":
            return block.split(" ", 1)[1].strip()

    raise Exception("No header!")
