from pathlib import Path

from open_cv.lib.ring_buffer import RingBuffer

"""
Functions to support image and video paths
"""

# imread supports
IMAGE_EXTS = (
    ".bmp",
    "*.dib",
    ".jpeg",
    ".jpg",
    ".jpe",
    ".jp2",
    ".png",
    ".pbm",
    ".pgm",
    ".ppm",
    ".sr",
    ".ras",
    ".tiff",
    ".tif",
)


def path_to_image_paths(path):
    path = Path(path)

    if path.is_dir():
        return RingBuffer(image_paths(path))

    if is_image_path(path):
        return RingBuffer(image_paths(path.parent), path)

    return RingBuffer(image_paths(path.parent))


def paths_to_image_paths(paths):
    """
    return a list of image Paths given a list of file and/or directory Paths
    """

    result = []
    for path in paths:

        path = Path(path)

        if path.is_dir():
            result.extend(image_paths(path))

        elif is_image_path(path):
            result.append(path)

    return result


def is_image_path(path):
    """ returns if path is a valid path for an image"""
    return path.is_file() and path.suffix.lower() in IMAGE_EXTS


def image_paths(directory_path=".", pattern="*"):
    """
    yield the next path to an image in directory_path
    that matches the pattern.
    """
    return file_paths(directory_path, valid_exts=IMAGE_EXTS, pattern=pattern)


def file_paths(directory_path, pattern="*", valid_exts=None):
    """
    yield the next path in directory_path
    that matches the pattern and 
    if specified, has a suffic contained in valid_exts
    """
    if type(directory_path) is str:
        directory_path = Path(directory_path)
    assert directory_path.is_dir()

    for path in Path(directory_path).glob(pattern):

        # if filename does not end in valid_ext, ignore it
        if valid_exts is not None and not path.suffix.lower() in valid_exts:
            continue

        yield path


def _test1(paths=()):
    return map(Path, paths)


def _test2(directory="."):
    return [path for path in Path(directory).iterdir() if path.is_file()]


def _test3(directory=".", pattern="**.*.py"):
    return Path(directory).glob(pattern)


'''
import os
from glob import glob

def image_paths(directory_path=".", contains=None):
    """ return the set of files that are valid """
    return file_paths(directory_path, valid_exts=IMAGE_EXTS, pattern=pattern)

def file_paths(directory_path, valid_exts=None, contains=None):
    for root_dir, dir_names, filenames in os.walk(directory_path):
        for filename in filenames:

            # if filename does not contain the contains string, ignore it
            if contains is not None and filename.find(contains) == -1:
                continue

            # if filename does not end in valid_ext, ignore it
            if valid_exts is not None and not filename.endswith(valid_exts):
                continue

            # construct the path to the image and yield it
            image_path = os.path.join(root_dir, filename)
            image_path = image_path.replace(" ", "\\ ")
            yield image_path


def files_in_directory(path=".", *patterns):
    if not patterns:
        patterns = ("*",)

    # find files for each pattern
    result = [glob(os.path.join(path, pattern)) for pattern in patterns]

    # merge sublists
    result = [item for sublist in result for item in sublist]

    # strip path
    n = len(path) + 1
    result = [item[n:] for item in result if os.path.isfile(item)]

    # return sorted list
    result.sort()
    return result


def prompt_image_file(prompt="Image: ", filename=None):
    path = data_path(".")
    if filename is None:
        files = files_in_directory(path, "*.png", "*.jpg", "*.gif", "*.tiff")
        filename = prompt_options(prompt, files)
    return os.path.join(path, filename)


def prompt_video_file(prompt="Video: ", filename=None):
    path = data_path("./videos")
    if filename is None:
        files = files_in_directory(path, "*.avi", "*.mp4")
        filename = prompt_options(prompt, files)
    return os.path.join(path, filename)


def prompt_image(prompt="Image: ", filename=None):
    return load(prompt_image_file(prompt, filename))
'''
