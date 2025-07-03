#!/usr/bin/env python3
"""
Entry point for the DICOM Visualization System package.

This module allows the package to be executed as a script using:
    python -m dicom_viewer [folder_path]
"""

import sys
import os
from .interfaces.patient_interface import patient_interface


def main():
    """Main entry point for the DICOM viewer application."""
    # Default folder path - users should modify this or add command line arguments
    default_folder_path = r'D:\TFG\estudios_ct'
    
    # Get the path from command line arguments or use default
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        folder_path = default_folder_path
    
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"Error: The specified folder '{folder_path}' does not exist.")
        print("Please provide a valid DICOM folder path.")
        print("Usage: python -m dicom_viewer [path_to_dicom_folder]")
        sys.exit(1)
    
    try:
        patient_interface(folder_path)
    except Exception as e:
        print(f"Error running DICOM viewer: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()