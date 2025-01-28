import os

from .copy_static import copy_static_files
from .generate_html import generate_pages_recursive


def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    static_dir = os.path.join(project_root, "static")
    public_dir = os.path.join(project_root, "public")
    template_path = os.path.join(project_root, "template.html")
    content_path = os.path.join(project_root, "content")
    output_path = os.path.join(public_dir)

    copy_static_files(static_dir, public_dir)
    generate_pages_recursive(content_path, template_path, output_path)


if __name__ == "__main__":
    main()
