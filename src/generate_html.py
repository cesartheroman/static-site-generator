import os

from .block_markdown import markdown_to_blocks, markdown_to_html_node


def extract_title(markdown: str) -> str:
    """
    Extracts the first header (h1) from markdown text.

    Args:
        markdown: Input markdown string

    Returns:
        The text content of the first h1 header

    Raises:
        Exception: If no header is found in the markdown
    """
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        if block.startswith("#") and len(block) > 1 and block[1] == " ":
            return block.split(" ", 1)[1].strip()

    raise Exception("No header!")


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    """
    Generates a single HTML page from markdown using a template.

    Args:
        from_path: Path to source markdown file
        template_path: Path to HTML template file
        dest_path: Destination path for generated HTML

    Notes:
        Template should contain {{ Title }} and {{ Content }} placeholders
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as file:
        markdown = file.read()

    extracted_title = extract_title(markdown)
    converted_md = markdown_to_html_node(markdown)

    with open(template_path) as template_file:
        template_content = template_file.read()

    html = template_content.replace("{{ Title }}", extracted_title).replace(
        "{{ Content }}", converted_md.to_html()
    )

    if dest_path:
        dir_path = os.path.dirname(dest_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(dest_path, "w") as output_file:
            output_file.write(html)


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    """
    Recursively converts markdown files in a directory to HTML pages.

    Args:
        dir_path_content: Source directory containing markdown files
        template_path: Path to HTML template file
        dest_dir_path: Destination directory for generated HTML files

    Raises:
        FileNotFoundError: If source directory doesn't exist

    Notes:
        Maintains directory structure in output
        Only processes .md files
        Template should contain {{ Title }} and {{ Content }} placeholders
    """
    if not os.path.exists(dir_path_content):
        raise FileNotFoundError(f"Source directory {dir_path_content} does not exist.")

    for file_name in os.listdir(dir_path_content):
        src_item = os.path.join(dir_path_content, file_name)

        if os.path.isfile(src_item) and os.path.splitext(src_item)[1] == ".md":
            base_name = os.path.splitext(file_name)[0]
            dst_item = os.path.join(dest_dir_path, base_name + ".html")

            with open(src_item) as file:
                markdown = file.read()

            extracted_title = extract_title(markdown)
            extracted_html_content = markdown_to_html_node(markdown).to_html()

            with open(template_path) as template_file:
                template_content = template_file.read()

            html = template_content.replace("{{ Title }}", extracted_title).replace(
                "{{ Content }}", extracted_html_content
            )

            dir_path = os.path.dirname(dst_item)
            os.makedirs(dir_path, exist_ok=True)

            with open(dst_item, "w") as output_file:
                output_file.write(html)

        elif os.path.isdir(src_item):
            dst_dir = os.path.join(dest_dir_path, file_name)
            generate_pages_recursive(src_item, template_path, dst_dir)
