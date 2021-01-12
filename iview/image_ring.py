#!/usr/bin/env python

"""
Display all images in paths
"""

import sys

from iview.image_paths import images_in_paths, imread
from iview.type_ext import FilePath, Image, List, Tuple
from lib.ring_buffer import RingBuffer


class ImageRing:
    def __init__(self, paths: List[FilePath], subdirectories: bool = False):

        first_image = None
        image_paths_ = images_in_paths(paths, subdirectories)
        if len(image_paths_) == 1:
            first_image = image_paths_[0]
            image_paths_ = images_in_paths([first_image.parent], subdirectories)
        if len(image_paths_) == 0:
            sys.exit(1)  # TODO: Error
        self._ring = RingBuffer(image_paths_, first_image)
        self._image_path = None
        self._image = None
        self._fetch()

    def __call__(self) -> Tuple[FilePath, Image]:
        return self._image.copy()

    @property
    def path(self):
        return self._image_path

    def _fetch(self) -> None:
        self._image_path = self._ring.value()
        self._image = imread(self._image_path)

    def next(self) -> None:
        self._ring.next_()
        self._fetch()

    def prev(self) -> None:
        self._ring.prev_()
        self._fetch()

    def pop(self) -> None:
        self._ring.pop()
        self._fetch()
