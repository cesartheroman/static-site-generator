import os
import shutil


def copy_static_files(src_path: str, dst_path: str):
    """
    Recursively copy all files and directories from source to destination.

    Completely replaces the destination directory if it exists.
    Creates the destination directory if it does not exist.

    Args:
        src_path (str): Source directory path to copy from
        dst_path (str): Destination directory path to copy to

    Raises:
        FileNotFoundError: If source directory does not exist
    """
    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Source directory {src_path} does not exist.")

    if os.path.exists(dst_path):
        shutil.rmtree(dst_path)

    os.makedirs(dst_path)

    for file_name in os.listdir(src_path):
        src_item = os.path.join(src_path, file_name)
        dst_item = os.path.join(dst_path, file_name)

        if os.path.isdir(src_item):
            copy_static_files(src_item, dst_item)
        else:
            shutil.copy(src_item, dst_item)


if __name__ == "__main__":
    src_path = os.path.join(os.getcwd(), "static")
    dst_path = os.path.join(os.getcwd(), "public")

    copy_static_files(src_path, dst_path)
