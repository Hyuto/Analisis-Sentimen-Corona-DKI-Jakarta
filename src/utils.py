import os
from datetime import datetime

import psutil


def get_name(path: str) -> str:
    """Menggenerate nama file yang valid di dalam suatu direktory agar tidak terjadi overwrite

    Args:
        path (str): file path

    Returns:
        str: full path dari nama file yang valid
    """
    if not os.path.exists(path):
        return path

    filename, extension = os.path.splitext(path)
    index = 1
    while True:
        new_name = f"{filename} ({index}){extension}"

        if not os.path.exists(new_name):
            return new_name
        else:
            index += 1


def datetime_validator(strd: str) -> None:
    """Validate string isoformated datetime.

    Args:
        strd (str): string isoformated datetime.

    Raises:
        ValueError: incorrect string datetime format.
    """
    try:
        datetime.fromisoformat(strd)
    except ValueError:  # pragma: no cover
        raise ValueError("Incorrect date format!")


def kill_proc_tree(pid: int) -> None:
    """Kill process

    Args:
        pid (int): pid
    """
    parent = psutil.Process(pid)
    children = parent.children(recursive=True)
    for child in children:
        child.kill()
    psutil.wait_procs(children, timeout=5)
