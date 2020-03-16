"""
Define commonly used types for type hinting
"""

from typing import Union, Optional, List, Tuple, Sequence
from pathlib import Path, PosixPath
import numpy as np

FilePath = Union[Path, PosixPath, str]
Color = Union[Tuple[int, ...], Tuple[float, ...]]
Image = np.ndarray
