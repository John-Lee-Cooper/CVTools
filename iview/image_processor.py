"""
Abstract image processor class
"""

from abc import abstractmethod

from iview.type_ext import Image


class ImageProcessor:
    """ Base class to manipulate images.  """

    def __init__(self, enabled: bool = True):
        self.enabled = enabled

    def toggle_enabled(self) -> None:
        """ Toggle enabled """
        self.enabled = not self.enabled

    @abstractmethod
    def __call__(self, image: Image, *args) -> Image:
        """ if enabled apply processing """
