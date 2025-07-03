# Project Structure

This document describes the improved organization of the DICOM Visualization System project.

## Directory Structure

```
dicom-viewer-python/
├── src/                          # Source code
│   └── dicom_viewer/            # Main package
│       ├── __init__.py          # Package initialization
│       ├── __main__.py          # Entry point for 'python -m dicom_viewer'
│       ├── core/                # Core functionality
│       │   ├── __init__.py
│       │   └── dicom_viewer.py  # Main DicomViewer class
│       ├── interfaces/          # User interface modules
│       │   ├── __init__.py
│       │   ├── patient_interface.py     # Patient selection interface
│       │   ├── study_interface.py       # Study selection interface
│       │   ├── preview_studies.py       # Study preview with images
│       │   └── preview_first_study.py   # First study preview
│       ├── utils/               # Utility functions
│       │   ├── __init__.py
│       │   ├── series_utils.py          # Series analysis utilities
│       │   └── image_utils.py           # Image processing utilities
│       └── data/                # Data handling
│           ├── __init__.py
│           ├── organize_images.py       # Image organization
│           └── metadata.py              # Metadata handling
├── docs/                        # Documentation
│   ├── README.md               # Main documentation
│   ├── PROJECT_STRUCTURE.md    # This file
│   ├── API_DOCUMENTATION.md    # API documentation
│   ├── COMPONENT_ARCHITECTURE.md # Architecture documentation
│   ├── DOCUMENTATION_INDEX.md  # Documentation index
│   └── QUICK_REFERENCE.md      # Quick reference guide
├── scripts/                     # Entry point scripts
│   └── main.py                 # Traditional main entry point
├── tests/                       # Future test files
├── requirements.txt            # Python dependencies
├── setup.py                    # Package setup configuration
├── .gitignore                  # Git ignore patterns
└── README.md                   # Project overview (link to docs/README.md)
```

## Package Organization

### Core (`src/dicom_viewer/core/`)
Contains the main DICOM viewing functionality:
- `DicomViewer` class: The main viewer with image display, navigation, and window/level controls

### Interfaces (`src/dicom_viewer/interfaces/`)
Contains all user interface components:
- Patient interface for selecting patients/studies
- Study interface for study selection
- Preview interfaces for visualizing studies before opening

### Utils (`src/dicom_viewer/utils/`)
Contains utility functions:
- Series analysis and unique series detection
- Image processing and enhancement utilities

### Data (`src/dicom_viewer/data/`)
Contains data handling functionality:
- Image organization and file management
- Metadata extraction and handling

## Installation

### Development Installation
```bash
# Clone the repository
git clone https://github.com/manuamest/dicom-viewer-python.git
cd dicom-viewer-python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
```

### Regular Installation
```bash
pip install .
```

## Usage

### Command Line
```bash
# Using the script
python scripts/main.py [path_to_dicom_folder]

# Using the package
python -m dicom_viewer [path_to_dicom_folder]

# Using the console entry point (after installation)
dicom-viewer [path_to_dicom_folder]
```

### Python Import
```python
from dicom_viewer import DicomViewer, patient_interface

# Use the viewer directly
viewer = DicomViewer(folder_path, series_number, thickness)
viewer.show_dicom()

# Use the patient interface
patient_interface('/path/to/dicom/folder')
```

## Benefits of This Structure

1. **Modularity**: Clear separation of concerns with dedicated packages for different functionality
2. **Scalability**: Easy to add new features without cluttering the main directory
3. **Maintainability**: Logical organization makes code easier to find and modify
4. **Standard Python Practices**: Follows Python packaging best practices
5. **Import Clarity**: Clear import paths that reflect the project structure
6. **Documentation**: Centralized documentation in the docs/ folder
7. **Testing**: Dedicated space for test files
8. **Distribution**: Proper setup.py for easy installation and distribution