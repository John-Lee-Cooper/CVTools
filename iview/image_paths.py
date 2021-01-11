"""
Functions to support image and video paths
"""

from pathlib import Path, PosixPath

import cv2 as cv
import numpy as np

from iview import ui
from iview.paths import file_paths
from iview.type_ext import FilePath, Image, List, Optional, Sequence

# imread supports
IMAGE_EXTS = (
    ".bmp .dib .jpeg .jpg .jpe .jp2 .webp .png .pbm .pgm .ppm .pxm .pnm .pfm "
    ".sr .ras .tif .tiff .exr .hdr .pic"
).split(" ")


def is_image_path(path: PosixPath) -> bool:
    """ Return if path is a valid path for an image"""
    return path.is_file() and path.suffix.lower() in IMAGE_EXTS


def image_paths(directory_path: FilePath = ".", pattern: str = "*") -> List[PosixPath]:
    """
    Return the paths to the images in directory_path that matches the pattern.
    """
    return file_paths(directory_path, pattern=pattern, valid_exts=IMAGE_EXTS)


def images_in_paths(
    paths: List[FilePath], subdirectories: bool = False
) -> Sequence[FilePath]:
    """
    Return a RingBuffer of image Paths given a list of file and/or directory Paths
    """

    pattern = "**/*" if subdirectories else "*"

    image_paths_ = []
    for path in paths:
        path = Path(path)
        if is_image_path(path):
            image_paths_.append(path)
        elif path.is_dir():
            image_paths_.extend(image_paths(path, pattern))
        else:
            ui.warning(
                f"path_to_image_paths(path): path:{path} is not a directory or image"
            )

    if not image_paths_:
        if len(paths) == 0:
            ui.warning("images_in_paths(paths): paths is empty")
        else:
            ui.warning(f"No images in {paths}")

    return image_paths_


def imread(file_name: FilePath, flags: int = cv.IMREAD_COLOR) -> Image:
    """
    Load an image from the specified file and returns it.
    Filename may be a Path.

    flags may be:
      IMREAD_COLOR = Default flag for imread. Loads color image.
      IMREAD_GRAYSCALE = Loads image as grayscale.
      IMREAD_UNCHANGED = Loads image which have alpha channels.
      IMREAD_ANYCOLOR = Loads image in any possible format
      IMREAD_ANYDEPTH = Loads image in 16-bit/32-bit else converts it to 8-bit
    """
    image = cv.imread(str(file_name), flags)  # str in case file_name is a Path

    if image is None:
        ui.error(f"Failed to load image file: {file_name}")

    return image


def imwrite(
    file_name: FilePath,
    image: np.ndarray,
    dir_path: Optional[FilePath] = None,
    params: Optional[int] = None,
) -> None:
    """
    Save image to file_name
    Filename may be a Path.
    If dir_path is provided, save image in that directory
    """
    if dir_path:
        file_name = Path(dir_path).parent / Path(file_name).name
    cv.imwrite(str(file_name), image, params)
