"""
Define commonly used types for type hinting
"""

from pathlib import PosixPath
from typing import Union, Optional, List, Iterator
import numpy as np

FilePath = Union[PosixPath, str]
Image = np.ndarray
