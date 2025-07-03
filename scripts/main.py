#!/usr/bin/env python3
"""
Main entry point for the DICOM Visualization System.

This script initializes and runs the DICOM viewer application.
"""

import sys
import os

# Add the src directory to the Python path to allow imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from dicom_viewer.interfaces.patient_interface import patient_interface


def main():
    """Main entry point for the DICOM viewer application."""
    # Default folder path - users should modify this or add command line arguments
    folder_path = r'D:\TFG\estudios_ct'
    
    # You can also get the path from command line arguments
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"Error: The specified folder '{folder_path}' does not exist.")
        print("Please provide a valid DICOM folder path.")
        print("Usage: python main.py [path_to_dicom_folder]")
        sys.exit(1)
    
    try:
        patient_interface(folder_path)
    except Exception as e:
        print(f"Error running DICOM viewer: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()