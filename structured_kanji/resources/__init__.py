import os
import pathlib


def get_resource_path() -> str:
    return str(pathlib.Path(__file__).parent.resolve())


def get_icon(icon_name: str):
    path = get_resource_path()
    return os.path.join(path, "icons", icon_name)
