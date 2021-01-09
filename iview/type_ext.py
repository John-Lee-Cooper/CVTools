"""
Define commonly used types for type hinting
"""

from pathlib import Path, PosixPath
from typing import (List, Optional, Sequence,  # pylint: disable=unused-import
                    Tuple, Union)

import numpy as np

FilePath = Union[Path, PosixPath, str]
Color = Union[Tuple[int, ...], Tuple[float, ...]]
Image = np.ndarray
