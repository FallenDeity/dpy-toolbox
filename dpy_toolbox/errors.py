import sys


class _Exception(Exception):
    def __init__(self, *args):
        self.exc = args

    def __call__(self, *args, **kwargs):
        sys.stderr.write(" ".join(args))

class NoEventFunction(_Exception):
    pass

class NotAllowed(_Exception):
    pass