"""Collection of built-in candlestick patterns."""

from .head_shoulders import ReverseHeadAndShoulders, HeadAndShoulders
from .wedge import RisingWedge, FallingWedge
from .double import DoubleBottom, DoubleTop
from .triangle import AscendingTriangle, DescendingTriangle, BullishTriangle, BearishTriangle

# Re-export pattern classes for convenience
__all__ = [
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

