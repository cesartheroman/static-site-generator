import os

from .copy_static import copy_static_files
from .utils import generate_page


def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    static_dir = os.path.join(project_root, "static")
    public_dir = os.path.join(project_root, "public")
    template_path = os.path.join(project_root, "template.html")
    content_path = os.path.join(project_root, "content", "index.md")
    output_path = os.path.join(public_dir, "index.html")

    copy_static_files(static_dir, public_dir)
    generate_page(content_path, template_path, output_path)


if __name__ == "__main__":
    main()
