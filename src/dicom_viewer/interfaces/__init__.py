"""
User interface modules.

Contains all UI-related functionality including patient interface, study interface,
and preview components.
"""

from .patient_interface import patient_interface
from .study_interface import show_series_data

__all__ = ["patient_interface", "show_series_data"]