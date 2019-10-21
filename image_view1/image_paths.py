""" """

from pathlib import Path
import cv2 as cv
import ui
from ring_buffer import RingBuffer
from paths import file_paths

"""
Functions to support image and video paths
"""

# imread supports
IMAGE_EXTS = ".bmp .dib .jpeg .jpg .jpe .jp2 .webp .png .pbm .pgm .ppm .pxm .pnm .pfm .sr .ras .tif .tiff .exr .hdr .pic".split(" ")


def imread(filename=None, mode=cv.IMREAD_COLOR):
    """
    Load an image from the specified file and returns it.
    Filename may be a Path.

    mode may be:
      IMREAD_COLOR = Default flag for imread. Loads color image.
      IMREAD_GRAYSCALE = Loads image as grayscale.
      IMREAD_UNCHANGED = Loads image which have alpha channels.
      IMREAD_ANYCOLOR = Loads image in any possible format
      IMREAD_ANYDEPTH = Loads image in 16-bit/32-bit else converts it to 8-bit
    """
    if filename is None:
        ui.error(f"Failed to load image file: None")

    image = cv.imread(str(filename), mode)  # str in case filename is a Path

    if image is None:
        ui.error(f"Failed to load image file: {filename}")

    return image


def imwrite(filename, image, dir_path=None):
    """
    Save image to filename
    Filename may be a Path.
    If dir_path is provided, save image in that directory
    """
    if dir_path:
        filename = Path(dir_path).parent / Path(filename).name
    cv.imwrite(str(filename), image)


def paths_to_image_ring(paths):
    """ Return a RingBuffer of image Paths given a list of file and/or directory Paths """

    if len(paths) == 0:
        ui.warning(f"paths_to_image_paths(paths): paths is empty")
        return []

    if len(paths) == 1:
        return path_to_image_ring(paths[0])

    image_paths_ = []
    for index, path in enumerate(paths):
        path = Path(path)
        if is_image_path(path):
            image_paths_.append(path)
        else:
            ui.warning(f"paths_to_image_paths(paths): paths[{index}] is not an image")

    if not image_paths_:
        ui.warning(f"No images in {paths}")
    return RingBuffer(image_paths_)


def path_to_image_ring(path, subdirectories=True):
    """ Return a RingBuffer of image Paths given a file or directory Path """
    path = Path(path)
    pattern = "**/*" if subdirectories else "*"

    if path.is_dir():
        image_ring = RingBuffer(image_paths(path, pattern))
    elif is_image_path(path):
        image_ring = RingBuffer(image_paths(path.parent, pattern), path)
    else:
        ui.warning(f"path_to_image_paths(path): path:{path} is not a directory or image")
        return []

    if not image_ring:
        ui.warning(f"No images in {path}")
    return image_ring


def is_image_path(path):
    """ Return if path is a valid path for an image"""
    return path.is_file() and path.suffix.lower() in IMAGE_EXTS


def image_paths(directory_path=".", pattern="*"):
    """
    Yield the next path to an image in directory_path that matches the pattern.
    """
    return file_paths(directory_path, pattern=pattern, valid_exts=IMAGE_EXTS)
