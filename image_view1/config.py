"""
Configure the tool
"""

from pathlib import Path
import keys

# Paths
DATA_PATH = Path("~/python/open_cv/data/").expanduser()
TRASH_PATH = Path("~/python/open_cv/data/trash/").expanduser()

# UI click styles
ERROR_STYLE = dict(fg="red", bold=True)
WARNING_STYLE = dict(fg="yellow", bold=True)
INFO_STYLE = dict(fg="green", bold=False)

# Keys
NEXT_KEY = keys.SPACE
PREV_KEY = keys.BACKSPACE
DELETE_KEYS = (keys.DELETE_KEY, ord("d"))
