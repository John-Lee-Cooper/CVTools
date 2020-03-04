#!/usr/bin/env python

"""
Display all images in paths
"""

import ui
from pathlib import Path
from type_ext import Tuple, List, FilePath, Image
from image_paths import images_in_paths, imread
from ring_buffer import RingBuffer


class ImageRing:
    def __init__(self, paths: List[FilePath], subdirectories: bool = False):

        first_image = None
        image_paths_ = images_in_paths(paths, subdirectories)
        if len(image_paths_) == 1:
            first_image = image_paths_[0]
            image_paths_ = images_in_paths([first_image.parent], subdirectories)
        if len(image_paths_) == 0:
            exit()
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
        self._ring.next()
        self._fetch()

    def prev(self) -> None:
        self._ring.prev()
        self._fetch()

    def pop(self) -> None:
        self._ring.pop()
        self._fetch()
