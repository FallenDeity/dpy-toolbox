import sys


class _Exception(Exception):
    """The base exception class all dpy-toolbox exceptions inherit from"""
    def __init__(self, *args):
        self.exc = args

    def __call__(self, *args, **kwargs):
        sys.stderr.write(" ".join(args))

class NoEventFunction(_Exception):
    """
    There is no function attached to the event
    """
    pass

class NotAllowed(_Exception):
    """
    A user was prevented from performing an action he was not allowed to perform
    """
    pass