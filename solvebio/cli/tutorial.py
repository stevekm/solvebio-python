import os
from pydoc import pager

TUTORIAL = os.path.abspath(os.path.dirname(__file__)) + '/tutorial.md'


def print_tutorial(args):
    pager(open(TUTORIAL, 'r+').read())