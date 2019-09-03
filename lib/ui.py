#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click


def error(message, exit_code=1):
    click.echo(message)
    exit(exit_code)


def warning(message):
    click.echo(message)


def info(message):
    click.echo(message)
