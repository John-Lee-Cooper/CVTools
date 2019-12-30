"""
Define commonly used types for type hinting
"""

from typing import Union, Optional, List, Tuple
from pathlib import PosixPath
import numpy as np

FilePath = Union[PosixPath, str]
Color = Tuple[int, float, complex]
Image = np.ndarray
