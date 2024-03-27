from __future__ import annotations
from typing import Callable

def read_file(
        filepath: str = "index",
        path_prefix: str = "web/",
        file_extension: str = ".html",
        replace_format: Callable = lambda k: f"[[{k}]]",
        **replace: dict[str, str]|str
    ) -> str:
    """
    Read a file from the filesystem and replace placeholders with the given values.

    :param filepath: The name of the file to read.
    :param path_prefix: The path prefix of the file.
    :param file_extension: The file extension of the file.
    :param replace_format: The format of the placeholders.
    :param replace: The values to replace the placeholders with.

    :return: The file content with the placeholders replaced.
    """

    data: str = ""
    path: str = path_prefix + filepath + file_extension

    with open(path, "r") as file:
        data = file.read()

    for key, value in replace.items():
        data = data.replace(replace_format(key), value) # type: ignore

    return data

