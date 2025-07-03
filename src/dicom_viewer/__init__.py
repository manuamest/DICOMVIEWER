"""
DICOM Visualization System

A Python-based DICOM file visualization and manipulation system designed for desktop environments.
Allows users to navigate through medical image series, adjust brightness and contrast (Window/Level),
and organize DICOM files by studies and patients.
"""

__version__ = "1.0.0"
__author__ = "DICOM Viewer Project"

# Import main classes and functions for easy access
from .core.dicom_viewer import DicomViewer
from .interfaces.patient_interface import patient_interface
from .interfaces.study_interface import show_series_data as study_show_series_data

__all__ = [
    "DicomViewer",
    "patient_interface",
    "study_show_series_data",
]