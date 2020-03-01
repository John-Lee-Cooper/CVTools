#!/usr/bin/env python

from pathlib import Path
from iview import App


if __name__ == "__main__":
    from sys import argv
    paths = [Path(arg) for arg in argv[1:]]
    App(paths).run()
