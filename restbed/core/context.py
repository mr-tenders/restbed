"""
Various context (RAII-like) classes for
use in a with-statement
"""

import pyinsane2

class PyInsaneContext(object):
    def __enter__(self):
        try:
            pyinsane2.init()
            return True
        except Exception:
            return False

    def __exit__(self, objtype, value, traceback):
        pyinsane2.exit()
