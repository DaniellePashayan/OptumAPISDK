"""Optum Claims API SDK.

Public entry point:
    from optumapisdk import OptumAPI
"""

from .Client import OptumAPI
from .exceptions import APIError

__all__ = ["OptumAPI", "APIError"]
