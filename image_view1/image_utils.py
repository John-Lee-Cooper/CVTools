"""
Functions to support manipulating numpy/open_cv images

TODO: Add doctests and/or demo
"""

import cv2 as cv
from type_ext import Image, Optional


def resize(
    image: Image,
    height: Optional[int] = None,
    width: Optional[int] = None,
    max_size: Optional[int] = None,
    max_height: Optional[int] = None,
    max_width: Optional[int] = None,
    interpolation: int = cv.INTER_AREA,
) -> Image:
    """
    Return image scaled using interpolation.
    The new size can be specified using height or width.
    The size can be further specified using max_width, max_height or max_size.
    The result will always have the same aspect ratio.
    """

    assert height is None or width is None
    assert (max_size is not None) + (max_height is not None) + (
        max_width is not None
    ) <= 1

    h, w = image.shape[:2]
    if height is not None:
        width = int(w * height / h)
    elif width is not None:
        height = int(h * width / w)
    else:
        height, width = h, w

    if max_size is not None and max(height, width) > max_size:
        if height > width:
            height = max_size
            width = int(w * height / h)
        else:
            width = max_size
            height = int(h * width / w)

    elif max_height is not None and height > max_height:
        height = max_height
        width = int(w * height / h)

    elif max_width is not None and width > max_height:
        width = max_width
        height = int(h * width / w)

    if width == w and height == h:  # No change
        return image

    # To shrink an image, it will generally look best with INTER_AREA.
    # To enlarge an image, it will generally look best with INTER_CUBIC interpolation.
    if interpolation is None:
        interpolation = cv.INTER_AREA if width <= w else cv.INTER_CUBIC

    return cv.resize(image, (width, height), interpolation=interpolation)
