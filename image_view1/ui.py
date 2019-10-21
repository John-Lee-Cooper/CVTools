#!/usr/bin/env python


try:  # Trying to find module on sys.path
    from click import secho
    import config

    click_installed = True
except ModuleNotFoundError:
    click_installed = False
    print("import click failed")


def error(message, exit_code=1):
    """ Notify user of a fatal error and exit with error_code """
    if click_installed:
        secho(message, **config.error_style)
    else:
        print(message)
    exit(exit_code)


def warning(message):
    """ Notify user something has gone wrong """
    if click_installed:
        secho(message, **config.warning_style)
    else:
        print(message)


def info(message):
    """ Notify user message"""
    if click_installed:
        secho(message, **config.info_style)
    else:
        print(message)


if __name__ == "__main__":
    info("info")
    warning("warning")
    error("error")
