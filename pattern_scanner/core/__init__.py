"""Core utilities and base classes for pattern recognition."""

from .abstract import AbstractPattern
from .util import get_crosspt
from .recognizer import PatternRecognizer

# Items made available when importing the core package
__all__ = [
    'AbstractPattern',
    'get_crosspt',
    'PatternRecognizer',
]

