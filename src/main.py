import os

from copy_static_files import copy_static_files


def main():
    src_path = os.path.join(os.getcwd(), "static")
    dst_path = os.path.join(os.getcwd(), "public")
    copy_static_files(src_path, dst_path)


if __name__ == "__main__":
    main()
