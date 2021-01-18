#!/usr/bin/env python

"""
Provide functions to write info, warning and error messages to the console.
"""

import sys

from click import secho

from iview import config


def error(message: str, exit_code: int = 1) -> None:
    """ Notify user of a fatal error and exit with error_code """
    secho(message, err=True, **config.ERROR_STYLE)
    sys.exit(exit_code)


def warning(message: str) -> None:
    """ Notify user something has gone wrong """
    secho(message, **config.WARNING_STYLE)


def info(message: str) -> None:
    """ Notify user message"""
    secho(message, **config.INFO_STYLE)


if __name__ == "__main__":
    info("info")
    warning("warning")
    error("error")
