"""
ElizaCog - OpenCog-ElizaOS Integration Module

This module provides the bridge between OpenCog AtomSpace and ElizaOS,
enabling cognitive excellence and seamless interoperability.
"""

__version__ = "1.0.0"
__author__ = "OpenCog Development Team"

from .cli import main
from .core import ElizaCogBridge
from .config import ElizaCogConfig

__all__ = ['main', 'ElizaCogBridge', 'ElizaCogConfig']