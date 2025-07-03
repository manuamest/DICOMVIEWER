"""
Data handling and organization modules.

Contains functionality for organizing DICOM files, metadata handling, and data processing.
"""

from .organize_images import organize_images
from .metadata import *

__all__ = ["organize_images"]