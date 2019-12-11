"""
"""

from type_ext import Image


class ImageProcessor:
    """ TODO """

    def __init__(self, enabled=True):
        self.enabled = enabled

    def toggle_enabled(self):
        """ TODO """
        self.enabled = not self.enabled

    def __call__(self, image: Image) -> Image:
        """
        if not self.enabled:
            return image
        return image
        """
