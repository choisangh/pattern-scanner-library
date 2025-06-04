
"""Expose common classes and patterns at the package level."""

from .__version__ import __version__

from .core import AbstractPattern, get_crosspt, PatternRecognizer
from .patterns import (
    ReverseHeadAndShoulders,
    HeadAndShoulders,
    RisingWedge,
    FallingWedge,
    DoubleBottom,
    DoubleTop,
    AscendingTriangle,
    DescendingTriangle,
    BullishTriangle,
    BearishTriangle,
)

# Public re-exports for easy access when importing the package
__all__ = [
    'AbstractPattern',
    'get_crosspt',
    'PatternRecognizer',
    'ReverseHeadAndShoulders',
    'HeadAndShoulders',
    'RisingWedge',
    'FallingWedge',
    'DoubleBottom',
    'DoubleTop',
    'AscendingTriangle',
    'DescendingTriangle',
    'BullishTriangle',
    'BearishTriangle',
]

