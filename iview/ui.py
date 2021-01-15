#!/usr/bin/env python

"""
Provide functions to write info, warning and error messages to the console.
"""

import sys

try:  # Trying to find module on sys.path
    from click import secho

    CLICK_INSTALLED = True
except ModuleNotFoundError:
    CLICK_INSTALLED = False

from iview import config


def _echo(message: str, style) -> None:
    """ Notify user of a fatal error and exit with error_code """
    if CLICK_INSTALLED:
        secho(message, style)
    else:
        print(message)


def error(message: str, exit_code: int = 1) -> None:
    """ Notify user of a fatal error and exit with error_code """
    _echo(message, config.ERROR_STYLE)
    sys.exit(exit_code)


def warning(message: str) -> None:
    """ Notify user something has gone wrong """
    _echo(message, config.WARNING_STYLE)


def info(message: str) -> None:
    """ Notify user message"""
    _echo(message, config.INFO_STYLE)


if __name__ == "__main__":
    info("info")
    warning("warning")
    error("error")
