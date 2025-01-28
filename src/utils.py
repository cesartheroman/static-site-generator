import os

from .block_markdown import markdown_to_blocks, markdown_to_html_node


def extract_title(markdown: str):
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        if block.startswith("#") and len(block) > 1 and block[1] == " ":
            return block.split(" ", 1)[1].strip()

    raise Exception("No header!")


def generate_page(from_path, template_path, dest_path):
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


if __name__ == "__main__":
    generate_page("../content/index.md", "../template.html", "../public/index.html")
