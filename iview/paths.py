"""
Extensions to pathlib
"""

from pathlib import Path
from sys import argv

from iview import config
from iview.type_ext import FilePath, List, Optional


def script_name() -> str:
    """ Return final path component of script without .py extension """
    return Path(argv[0]).stem


def file_paths(
    directory_path: FilePath,
    pattern: str = "*",
    valid_exts: Optional[List[str]] = None,
) -> List[Path]:
    """
    Yield the next path in directory_path that matches the pattern and
    if specified, has a suffix contained in valid_exts
    """
    directory_path = Path(directory_path)
    assert directory_path.is_dir()

    valid_exts = [ext.lower() for ext in valid_exts] if valid_exts else []

    # if filename does not end in valid_ext, ignore it
    result = [
        path
        for path in directory_path.glob(pattern)
        if path.is_file() and path.suffix.lower() in valid_exts
    ]

    result.sort()
    return result


def trash(path: FilePath) -> None:
    """
    Move path to trash directory (safe delete)
    If path already exists there, try adding a number (1) to the end of the name
    and increment it until a unique path is found.
    """
    src_path = Path(path)
    dst_path = config.TRASH_PATH / src_path.name

    # Ensure we are not overwriting anything in trash
    count = 1
    while dst_path.exists():
        count += 1
        dst_path = dst_path.parent / f"{dst_path.stem}_{count}{dst_path.suffix}"

    src_path.replace(dst_path)
