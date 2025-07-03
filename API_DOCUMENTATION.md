# DICOM Visualization System - API Documentation

## Overview

The DICOM Visualization System is a Python-based medical image viewer designed for navigating and analyzing DICOM (Digital Imaging and Communications in Medicine) files. This documentation covers all public APIs, functions, and components available in the system.

## Table of Contents

1. [DicomViewer Class](#dicomviewer-class)
2. [Patient Interface Module](#patient-interface-module)
3. [Preview Studies Module](#preview-studies-module)
4. [Study Interface Module](#study-interface-module)
5. [Unique Series Module](#unique-series-module)
6. [Preview First Study Module](#preview-first-study-module)
7. [Metadata Module](#metadata-module)
8. [Usage Examples](#usage-examples)
9. [Error Handling](#error-handling)

---

## DicomViewer Class

**File:** `dicom_viewer.py`

The core class for DICOM image visualization with navigation and window/level adjustment capabilities.

### Constructor

#### `DicomViewer(folder_path, series_number, thickness, fig=None)`

Creates a new DICOM viewer instance.

**Parameters:**
- `folder_path` (str): Path to the folder containing DICOM files
- `series_number` (str): DICOM series number to display
- `thickness` (float): Slice thickness for filtering images
- `fig` (matplotlib.figure.Figure, optional): Matplotlib figure object. If None, creates a new figure

**Example:**
```python
from dicom_viewer import DicomViewer
import matplotlib.pyplot as plt

viewer = DicomViewer('/path/to/dicom/files', '301', 0.3)
viewer.show_dicom()
plt.show()
```

### Public Methods

#### `load_studies()`

Loads and organizes DICOM studies from the specified folder path.

**Returns:**
- `list`: List of study dictionaries containing file information, window settings, and metadata

**Functionality:**
- Filters files by series number and thickness
- Extracts window width and center values
- Sorts files by instance number
- Groups files by thickness values

#### `load_dicom(file_name)`

Loads pixel data from a specific DICOM file.

**Parameters:**
- `file_name` (str): Name of the DICOM file to load

**Returns:**
- `numpy.ndarray`: Pixel array data from the DICOM file

#### `show_dicom(image=None)`

Displays the current DICOM image with proper window/level settings.

**Parameters:**
- `image` (numpy.ndarray, optional): Image data to display. If None, loads current image

**Functionality:**
- Applies window/level settings for optimal contrast
- Displays image title with navigation information
- Shows current window/level values

#### `next_dicom()`

Navigates to the next DICOM image in the current study.

**Usage:**
- Increments the current image index
- Automatically refreshes the display
- Handles boundary conditions (stops at last image)

#### `prev_dicom()`

Navigates to the previous DICOM image in the current study.

**Usage:**
- Decrements the current image index
- Automatically refreshes the display
- Handles boundary conditions (stops at first image)

#### `increase_window_width()`

Increases the window width by 100 units for enhanced contrast range.

**Effect:**
- Widens the grayscale display range
- Affects all studies in the viewer
- Automatically refreshes the display

#### `decrease_window_width()`

Decreases the window width by 100 units for narrower contrast range.

**Effect:**
- Narrows the grayscale display range
- Maintains minimum width at window center value
- Automatically refreshes the display

#### `increase_window_center()`

Increases the window center by 100 units for brighter display.

**Effect:**
- Shifts the brightness level upward
- Affects all studies in the viewer
- Automatically refreshes the display

#### `decrease_window_center()`

Decreases the window center by 100 units for darker display.

**Effect:**
- Shifts the brightness level downward
- Maintains minimum center value of 0
- Automatically refreshes the display

### Event Handlers

#### `on_scroll(event)`

Handles mouse scroll events for image navigation.

**Parameters:**
- `event`: Matplotlib scroll event object

**Behavior:**
- Scroll down: Next image
- Scroll up: Previous image

#### `on_key(event)`

Handles keyboard events for navigation and window/level adjustment.

**Parameters:**
- `event`: Matplotlib key press event object

**Key Mappings:**
- `↓` (down arrow): Next image
- `↑` (up arrow): Previous image
- `i`: Increase window width
- `k`: Decrease window width
- `j`: Increase window center
- `l`: Decrease window center

---

## Patient Interface Module

**File:** `pacientInterface.py`

Provides the main entry point for patient selection and study navigation.

### Functions

#### `show_series_folders(folder_path, series_data)`

Creates a GUI window displaying available patients as buttons.

**Parameters:**
- `folder_path` (str): Root path containing patient folders
- `series_data` (list): List of patient folder names

**Functionality:**
- Creates a 426x240 pixel window
- Displays one button per patient
- Each button opens the patient's studies

**Example:**
```python
from pacientInterface import show_series_folders

patients = ['Patient001', 'Patient002', 'Patient003']
show_series_folders('/medical/data/path', patients)
```

#### `show_studies_in_folder(root_folder, folder_name)`

Opens the study preview interface for a specific patient.

**Parameters:**
- `root_folder` (str): Root directory path
- `folder_name` (str): Patient folder name

**Functionality:**
- Constructs full patient folder path
- Launches preview studies interface

#### `pacientInterface(folder_path)`

Main entry point for the patient interface application.

**Parameters:**
- `folder_path` (str): Path to the directory containing patient folders

**Returns:**
- None (launches GUI application)

**Validation:**
- Checks if folder path exists
- Filters only valid directories
- Displays error message for invalid paths

**Example:**
```python
from pacientInterface import pacientInterface

# Launch the patient selection interface
pacientInterface('/path/to/medical/data')
```

---

## Preview Studies Module

**File:** `previewStudies.py`

Provides thumbnail preview functionality for DICOM studies with enhanced visualization.

### Functions

#### `load_dicom_image(file_path, scale_factor=4)`

Loads and processes a DICOM image for thumbnail display.

**Parameters:**
- `file_path` (str): Path to the DICOM file
- `scale_factor` (int, optional): Factor to scale down the image (default: 4)

**Returns:**
- `tuple`: (ImageTk.PhotoImage, width, height) or (None, 0, 0) if no pixel data

**Processing:**
- Applies contrast enhancement for images with slice thickness
- Scales image down by the specified factor
- Converts to format suitable for Tkinter display

**Example:**
```python
from previewStudies import load_dicom_image

img, width, height = load_dicom_image('/path/to/dicom/file.dcm', scale_factor=4)
if img:
    print(f"Loaded image: {width}x{height}")
```

#### `increase_contrast(image)`

Applies contrast enhancement to improve image visibility.

**Parameters:**
- `image` (numpy.ndarray): Input image array

**Returns:**
- `numpy.ndarray`: Contrast-enhanced image (0-255 range)

**Algorithm:**
1. Normalizes image to 0-1 range
2. Applies power function (γ=0.5) for enhancement
3. Scales back to 0-255 range

#### `create_button(folder_path, root, button_text, img_path, series_number, thickness, series_data, row, col, img_list)`

Creates a clickable button with DICOM thumbnail and study information.

**Parameters:**
- `folder_path` (str): Path to DICOM files
- `root` (tkinter.Widget): Parent widget
- `button_text` (str): Text to display on button
- `img_path` (str): Path to image file
- `series_number` (str): DICOM series number
- `thickness` (float): Slice thickness
- `series_data` (dict): Study metadata
- `row` (int): Grid row position
- `col` (int): Grid column position
- `img_list` (list): List to store image references

**Functionality:**
- Loads and displays thumbnail image
- Creates clickable button that opens full viewer
- Maintains image references to prevent garbage collection

#### `show_series_data(folder_path, series_data)`

Displays a grid of study thumbnails with navigation capabilities.

**Parameters:**
- `folder_path` (str): Path to DICOM files
- `series_data` (dict): Dictionary containing series information

**Grid Layout:**
- Dynamic column calculation based on study count
- 5-8 columns depending on total studies
- Responsive layout for optimal viewing

**Study Organization:**
- Groups by series number and thickness
- Includes studies without thickness information
- Displays series descriptions

#### `previewStudies(folder_path)`

Main function to launch the study preview interface.

**Parameters:**
- `folder_path` (str): Path to directory containing DICOM files

**Functionality:**
- Scans folder for DICOM files
- Organizes studies by series and thickness
- Associates thumbnail images with studies
- Launches preview interface

**Example:**
```python
from previewStudies import previewStudies

# Launch study preview for a patient
previewStudies('/path/to/patient/dicom/files')
```

---

## Study Interface Module

**File:** `studyInterface.py`

Provides a text-based interface for study selection without thumbnails.

### Functions

#### `show_series_data(folder_path, series_data)`

Creates a GUI with text-based buttons for study selection.

**Parameters:**
- `folder_path` (str): Path to DICOM files
- `series_data` (dict): Dictionary containing series metadata

**Button Layout:**
- Fixed size: 30 characters wide, 5 lines height
- 3 columns per row
- Grid-based positioning

**Information Displayed:**
- Series number and thickness (formatted to 2 decimals)
- Series description
- Special handling for studies without thickness

**Example:**
```python
from studyInterface import show_series_data
from uniqueSeries import find_unique_series_numbers_and_thicknesses

folder_path = '/path/to/dicom/files'
series_data = find_unique_series_numbers_and_thicknesses(folder_path)
show_series_data(folder_path, series_data)
```

---

## Unique Series Module

**File:** `uniqueSeries.py`

Provides utilities for analyzing and organizing DICOM series data.

### Functions

#### `find_unique_series_numbers_and_thicknesses(folder_path)`

Analyzes DICOM files to extract unique series numbers and thickness values.

**Parameters:**
- `folder_path` (str): Path to directory containing DICOM files

**Returns:**
- `dict`: Dictionary with series numbers as keys and metadata as values

**Data Structure:**
```python
{
    'series_number': {
        'thicknesses': set([thickness1, thickness2, ...]),
        'no_thickness': [file1, file2, ...],
        'series_description': 'Description text'
    }
}
```

**Processing:**
- Scans all .dcm files in directory
- Extracts series number, thickness, and description
- Groups files by series and thickness
- Handles files without thickness information

**Example:**
```python
from uniqueSeries import find_unique_series_numbers_and_thicknesses

series_data = find_unique_series_numbers_and_thicknesses('/path/to/dicom')
for series_num, data in series_data.items():
    print(f"Series {series_num}: {len(data['thicknesses'])} thickness variations")
```

#### `show_dicom_study(folder_path, series_number, thickness)`

Launches the DICOM viewer for a specific study.

**Parameters:**
- `folder_path` (str): Path to DICOM files
- `series_number` (str): Series number to display
- `thickness` (float): Slice thickness for filtering

**Functionality:**
- Creates new matplotlib figure
- Initializes DicomViewer instance
- Displays first image in series
- Enables interactive navigation

**Example:**
```python
from uniqueSeries import show_dicom_study

# Open a specific study
show_dicom_study('/path/to/dicom', '301', 0.3)
```

---

## Preview First Study Module

**File:** `preview1stStudy.py`

Simplified interface showing only the first available study as a preview.

### Functions

#### `load_dicom_image(file_path, scale_factor=4)`

Loads and scales a DICOM image for display (alternative implementation).

**Parameters:**
- `file_path` (str): Path to DICOM file
- `scale_factor` (int, optional): Scaling factor (default: 4)

**Returns:**
- `tuple`: (ImageTk.PhotoImage, width, height) or (None, 0, 0)

**Processing:**
- Linear scaling to 0-255 range
- Image resizing for thumbnail display
- PIL/Tkinter format conversion

#### `show_series_data(folder_path, series_data)`

Displays only the first study as a clickable thumbnail.

**Parameters:**
- `folder_path` (str): Path to DICOM files
- `series_data` (dict): Series metadata dictionary

**Functionality:**
- Shows single study thumbnail
- Simplified interface for quick access
- Maintains full functionality for selected study

---

## Metadata Module

**File:** `metadatos.py`

Simple utility for displaying DICOM metadata.

### Usage

This module provides a basic script for examining DICOM file metadata:

```python
import pydicom

# Load and display DICOM metadata
file_path = "path/to/dicom/file.dcm"
ds = pydicom.dcmread(file_path)
print(ds)  # Displays all metadata tags
```

**Functionality:**
- Loads DICOM file using pydicom
- Displays complete metadata structure
- Useful for debugging and analysis

---

## Usage Examples

### Basic DICOM Viewing

```python
from dicom_viewer import DicomViewer
import matplotlib.pyplot as plt

# Create viewer for specific series
viewer = DicomViewer('/path/to/dicom', '301', 0.3)
viewer.show_dicom()
plt.show()

# Navigate programmatically
viewer.next_dicom()
viewer.prev_dicom()

# Adjust window/level
viewer.increase_window_width()
viewer.increase_window_center()
```

### Patient Selection Interface

```python
from pacientInterface import pacientInterface

# Launch patient selection
pacientInterface('/medical/data/root')
```

### Study Analysis

```python
from uniqueSeries import find_unique_series_numbers_and_thicknesses
from previewStudies import previewStudies

# Analyze available studies
folder_path = '/path/to/patient/data'
series_data = find_unique_series_numbers_and_thicknesses(folder_path)

# Display analysis results
for series_num, data in series_data.items():
    print(f"Series {series_num}:")
    print(f"  Description: {data['series_description']}")
    print(f"  Thicknesses: {list(data['thicknesses'])}")
    print(f"  Files without thickness: {len(data['no_thickness'])}")

# Launch preview interface
previewStudies(folder_path)
```

### Custom Image Processing

```python
from previewStudies import load_dicom_image, increase_contrast
import numpy as np

# Load and process image
img_tk, width, height = load_dicom_image('/path/to/file.dcm')

# Custom contrast adjustment
ds = pydicom.dcmread('/path/to/file.dcm')
raw_image = ds.pixel_array
enhanced_image = increase_contrast(raw_image)
```

---

## Error Handling

### Common Error Scenarios

#### Invalid File Paths
```python
from pacientInterface import pacientInterface

# The function validates paths and shows error messages
pacientInterface('/invalid/path')  # Prints "Invalid folder path."
```

#### Missing DICOM Data
```python
from dicom_viewer import DicomViewer

# The viewer handles missing pixel data gracefully
viewer = DicomViewer('/path/with/invalid/files', '301', 0.3)
viewer.show_dicom()  # Shows "No se encontraron archivos DICOM válidos"
```

#### File Loading Errors
- DICOM files without pixel data return None values
- Invalid series numbers result in empty study lists
- Missing thickness information is handled separately

### Best Practices

1. **Always validate paths** before passing to interface functions
2. **Check return values** from image loading functions
3. **Handle empty study lists** in custom implementations
4. **Use try-catch blocks** when working with DICOM files directly

### Debugging Tips

1. **Use metadata module** to inspect DICOM file structure
2. **Check series data** with `find_unique_series_numbers_and_thicknesses()`
3. **Verify file extensions** (must be .dcm)
4. **Ensure proper file permissions** for reading DICOM files

---

## Dependencies

- **pydicom**: DICOM file reading and metadata extraction
- **matplotlib**: Image display and interactive navigation
- **tkinter**: GUI interface components
- **PIL (Pillow)**: Image processing and format conversion
- **numpy**: Numerical operations and array handling

## Installation Requirements

```bash
pip install pydicom matplotlib pillow numpy
```

Note: tkinter is typically included with Python standard library.