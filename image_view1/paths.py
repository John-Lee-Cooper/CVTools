from sys import argv
from pathlib import Path
import config
from type_ext import FilePath, Optional, List, Iterator, PosixPath

"""
Functions to support image and video paths
"""


def script_name() -> str:
    """ Return final path component of script without .py extension """
    return Path(argv[0]).stem


def trash(path: FilePath) -> None:
    """
    Move path to trash directory (safe delete)
    If path already exists there, try adding a number (1) to the end of the name
    and increment it until a unique path is found.
    """
    src_path = Path(path)
    dst_path = config.trash_path / src_path.name

    # Ensure we are not overwriting anything in trash
    count = 1
    while dst_path.exists():
        count += 1
        dst_path = dst_path.parent / f"{dst_path.stem}_{count}{dst_path.suffix}"

    src_path.replace(dst_path)


def file_paths(
    directory_path: FilePath, pattern: str = "*", valid_exts: Optional[List[str]] = None
) -> Iterator[PosixPath]:
    """
    Yield the next path in directory_path that matches the pattern and
    if specified, has a suffic contained in valid_exts
    """
    directory_path = Path(directory_path)
    assert directory_path.is_dir()

    for path in sorted(directory_path.glob(pattern)):

        # if filename does not end in valid_ext, ignore it
        if valid_exts is None or path.suffix.lower() in valid_exts:
            yield path
