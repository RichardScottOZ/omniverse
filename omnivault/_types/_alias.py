"""
This file contains aliases for common types.
"""
from __future__ import annotations

from typing_extensions import TypeAlias

from omnivault._types._sentinel import _NotGiven

NonNegativeInt: TypeAlias = int
PositiveInt: TypeAlias = int
Loss: TypeAlias = float
Accuracy: TypeAlias = float
Token: TypeAlias = str
NotGiven: TypeAlias = _NotGiven
