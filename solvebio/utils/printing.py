# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import locale
import logging

logger = logging.getLogger('solvebio')

try:
    # Switch from the default input ASCII encoding to the default locale.
    # The Python runtime will use this  it has to decode a
    # string buffer to unicode. This is not needed in Python3.

    # However reload(sys), used below resets stdin, stdout, and stderr
    # which is bad if they've already been reassigned. An ipython
    # notebook shell, for example, sets up its own stdout.
    # See github issue #43 and #21.
    std_handles = [sys.stdin, sys.stdout, sys.stderr]
    reload(sys).setdefaultencoding(locale.getdefaultlocale()[1])
    locale.setlocale(locale.LC_ALL, '')
except:
    pass
finally:
    sys.stdin, sys.stdout, sys.stderr = std_handles


# Set rows and columns and colors


def set_from_env(name, default_value):
    try:
        return int(os.environ[name])
    except:
        return default_value


TTY_ROWS = set_from_env('LINES', 24)
TTY_COLS = set_from_env('COLUMNS', 80)

TTY_COLORS = True

if sys.stdout.isatty():
    try:
        with open(os.devnull, 'w') as fnull:
            rows, cols = subprocess.check_output(
                ['stty', 'size'],
                stderr=fnull).split()
            TTY_ROWS = int(rows)
            TTY_COLS = int(cols)
    except:
        logger.warn('Cannot detect terminal column width.\nUsing value '
                    'from environment variables and/or internal defaults.')
else:
    TTY_COLORS = False


def pretty_int(num):
    return locale.format("%d", int(num), grouping=True)


# Basic color support

def green(text):
    if not TTY_COLORS:
        return text
    return '\033[32m' + text + '\033[39m'


def red(text):
    if not TTY_COLORS:
        return text
    return '\033[31m' + text + '\033[39m'


def yellow(text):
    if not TTY_COLORS:
        return text
    return '\033[33m' + text + '\033[39m'


def blue(text):
    if not TTY_COLORS:
        return text
    return '\033[34m' + text + '\033[39m'


def solve_bio():
    return blue('SolveBio')
