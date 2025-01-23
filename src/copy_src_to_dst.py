"""
Write a recursive function that copies all the contents from a source directory to a destination directory (in our case, static to public)
It should first delete all the contents of the destination directory to ensure that the copy is clean.
It should copy all files and subdirectories, nested files, etc.
I recommend logging the path of each file you copy, so you can see what's happening as you run and debug your code.
Here are some of the standard library docs that might be helpful:

os.path.exists
os.listdir
os.path.join
os.path.isfile
os.mkdir
shutil.copy
shutil.rmtree
"""

import os
import shutil


# TODO: figure out how to handle copying with the same structure in mind
# also how to delete dst path just once
def recursive_function(src_path: str, dst_path: str):
    print("src_path:", src_path)  # static
    print("dst_path:", dst_path)  # public

    if os.path.exists(dst_path):
        shutil.rmtree(dst_path)

    if not os.path.isdir(src_path):
        shutil.copy(src_path, dst_path)
        print("copied!", src_path.split("/")[-1])
    else:
        for file_name in os.listdir(src_path):
            print("file_name:", file_name)

            file_path = os.path.join(src_path, file_name)
            print("file_path in dir:", file_path)

            if os.path.exists(file_path):
                print("it exists!")

            print("call recursive_function")
            recursive_function(file_path, dst_path)

    return

    # os.path.exists("")
    # files_in_dir = os.listdir()
    # joined_paths = os.path.join("")
    # os.mkdir("")
    # new_dst = shutil.copy("../static/", "../public/")
    # shutil.rmtree("")


if __name__ == "__main__":
    src_path = os.path.join(os.getcwd(), "static")
    dst_path = os.path.join(os.getcwd(), "public")
    # src_path = os.path.join(os.getcwd(), "src", "test.txt")
    # dst_path = os.path.join(os.getcwd(), "src", "test1.txt")

    recursive_function(src_path, dst_path)
