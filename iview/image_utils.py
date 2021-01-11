"""
Support manipulating numpy/open_cv images
"""

import platform

import cv2 as cv
import numpy as np

from iview import config
from iview.image_processor import ImageProcessor
from iview.type_ext import Image, Optional, Tuple

if platform.system() == "Windows":

    def screen_size() -> Tuple[int, int]:
        import ctypes  # pylint: disable=import-outside-toplevel

        user32 = ctypes.windll.user32
        # screen_w, screen_h = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        screen_w, screen_h = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
        return screen_w, screen_h


else:

    def screen_size() -> Tuple[int, int]:
        from pymouse import PyMouse  # pylint: disable=import-outside-toplevel

        # from pykeyboard import PyKeyboard

        screen_w, screen_h = PyMouse().screen_size()
        return int(screen_w), int(screen_h)


class FitCanvas(ImageProcessor):
    """ Resize image to fit canvas without changing aspect ratio """

    def __init__(
        self,
        width: int,
        height: int,
        interpolation: int = cv.INTER_CUBIC,
        enabled: bool = False,
        matte_color: Optional[Tuple] = config.MATTE_COLOR,
        matte_size: int = config.MATTE_SIZE,
    ):
        super().__init__(enabled)

        self.canvas_w, self.canvas_h = width, height
        self.interpolation = interpolation
        self.matte_color = matte_color
        self.matte_size = matte_size

    def __call__(self, image: Image, *args) -> Image:
        """
        Return image of size height, width.
        The input image is scaled using interpolation.
        The result will always have the same aspect ratio as original image.
        """
        h, w = image.shape[:2]

        if not self.enabled:  # and h <= height and w <= width:
            return image

        height = self.canvas_h
        width = self.canvas_w
        scale_factor = min(height / h, width / w)
        scaled_width = int(w * scale_factor)
        scaled_height = int(h * scale_factor)

        if self.matte_color is None:
            return cv.resize(
                image, (scaled_width, scaled_height), interpolation=self.interpolation
            )

        scaled_width = min(scaled_width, width - self.matte_size)
        scaled_height = min(scaled_height, height - self.matte_size)
        depth = image.shape[2] if len(image.shape) == 3 else 1
        result = np.empty((height, width, depth), image.dtype)
        result[:] = self.matte_color
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
