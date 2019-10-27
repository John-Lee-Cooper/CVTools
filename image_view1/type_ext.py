"""
Define commonly used types for type hinting
"""

from typing import Union, Optional, List
from pathlib import PosixPath
import numpy as np

FilePath = Union[PosixPath, str]
Image = np.ndarray
