"""
Support manipulating numpy/open_cv images
"""

import numpy as np
import cv2 as cv
from pymouse import PyMouse

# from pykeyboard import PyKeyboard

from image_processor import ImageProcessor
from type_ext import Image


class FullScreen(ImageProcessor):
    """ Resize image to fit screen without changing aspect ratio """

    def __init__(self, interpolation: int = cv.INTER_CUBIC, enabled: bool = False):
        super().__init__(enabled)

        screen_w, screen_h = PyMouse().screen_size()
        self.screen_w = int(screen_w)
        self.screen_h = int(screen_h)
        self.interpolation = interpolation

    def __call__(self, image: Image) -> Image:
        """
        Return image of size height, width.
        The input image is scaled using interpolation.
        The result will always have the same aspect ratio as original image.
        """
        h, w = image.shape[:2]

        if not self.enabled and h <= self.screen_h and w <= self.screen_w:
            return image

        depth = image.shape[2] if len(image.shape) == 3 else 2

        height = self.screen_h
        width = self.screen_w
        result = np.zeros((height, width, depth), image.dtype)

        scale_factor = min(height / h, width / w)
        scaled_width = int(w * scale_factor)
        scaled_height = int(h * scale_factor)
        h_pad = (width - scaled_width) // 2
        v_pad = (height - scaled_height) // 2
        l, r = h_pad, h_pad + scaled_width
        t, b = v_pad, v_pad + scaled_height
        cv.resize(
            image,
            (scaled_width, scaled_height),
            dst=result[t:b, l:r, :],
            interpolation=self.interpolation,
        )

        return result
