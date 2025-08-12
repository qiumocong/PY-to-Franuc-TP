"""
PY-to-Franuc-TP: Python library for writing Fanuc robot teach pendant programs.

This library provides a Python interface for generating Fanuc TP (Teach Pendant)
programs programmatically, including all major robot programming commands.
"""

from .tp_writer import FanucTPWriter
from .position import Position
from .commands import *

__version__ = "1.0.0"
__author__ = "PY-to-Franuc-TP Project"

__all__ = [
    'FanucTPWriter',
    'Position',
    'MovementCommand',
    'LogicCommand',
    'IOCommand',
    'WaitCommand',
    'CallCommand'
]