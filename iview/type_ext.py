"""
Define commonly used types for type hinting
"""

from pathlib import Path, PosixPath
from typing import Sequence, List, Optional, Tuple, Union  # pylint: disable=unused-import

import numpy as np

FilePath = Union[Path, PosixPath, str]
Color = Union[Tuple[int, ...], Tuple[float, ...]]
Image = np.ndarray
