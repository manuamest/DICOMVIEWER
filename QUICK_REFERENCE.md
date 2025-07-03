# DICOM Viewer - Quick Reference Guide

## Quick Start

### Launch the Application
```bash
python main.py
```

### Basic Workflow
1. **Select Patient** → Click patient button in main interface
2. **Choose Study** → Click study thumbnail or text button
3. **Navigate Images** → Use arrow keys or scroll wheel
4. **Adjust Display** → Use keyboard shortcuts for window/level

---

## Keyboard Shortcuts

### Navigation
| Key | Action |
|-----|--------|
| `↑` | Previous image |
| `↓` | Next image |
| **Mouse Scroll** | Navigate images |

### Window/Level Adjustment
| Key | Action | Effect |
|-----|--------|--------|
| `i` | Increase window width | Wider contrast range |
| `k` | Decrease window width | Narrower contrast range |
| `j` | Increase window center | Brighter display |
| `l` | Decrease window center | Darker display |

---

## Common Code Snippets

### Basic DICOM Viewing
```python
from dicom_viewer import DicomViewer
import matplotlib.pyplot as plt

# Create and display viewer
viewer = DicomViewer('/path/to/dicom', '301', 0.3)
viewer.show_dicom()
plt.show()
```

### Launch Patient Interface
```python
from pacientInterface import pacientInterface
pacientInterface('/path/to/medical/data')
```

### Analyze Study Data
```python
from uniqueSeries import find_unique_series_numbers_and_thicknesses

series_data = find_unique_series_numbers_and_thicknesses('/path/to/dicom')
for series_num, data in series_data.items():
    print(f"Series {series_num}: {data['series_description']}")
```

### Load Single Image
```python
from previewStudies import load_dicom_image

img, width, height = load_dicom_image('/path/to/file.dcm')
```

---

## File Structure

```
DICOM-Viewer/
├── main.py                 # Application entry point
├── dicom_viewer.py         # Core viewer class
├── pacientInterface.py     # Patient selection
├── previewStudies.py       # Thumbnail interface
├── studyInterface.py       # Text-based interface
├── uniqueSeries.py         # Data processing utilities
├── preview1stStudy.py      # Single study preview
├── metadatos.py           # Metadata inspection
└── docs/
    ├── API_DOCUMENTATION.md
    ├── COMPONENT_ARCHITECTURE.md
    └── QUICK_REFERENCE.md
```

---

## Function Quick Reference

### DicomViewer Class
```python
# Constructor
DicomViewer(folder_path, series_number, thickness, fig=None)

# Navigation
viewer.next_dicom()        # Next image
viewer.prev_dicom()        # Previous image

# Window/Level
viewer.increase_window_width()    # Widen contrast
viewer.decrease_window_width()    # Narrow contrast
viewer.increase_window_center()   # Brighten
viewer.decrease_window_center()   # Darken

# Display
viewer.show_dicom()        # Refresh display
viewer.load_dicom(filename)  # Load specific image
```

### Interface Functions
```python
# Patient selection
pacientInterface(folder_path)

# Study preview
previewStudies(folder_path)

# Direct study launch
show_dicom_study(folder_path, series_number, thickness)

# Data analysis
find_unique_series_numbers_and_thicknesses(folder_path)
```

---

## Common Parameters

### Folder Paths
- **Root Data Path**: Main directory containing patient folders
- **Patient Path**: Individual patient directory
- **Study Path**: Directory containing DICOM files

### DICOM Parameters
- **Series Number**: Identifies specific imaging series (string)
- **Thickness**: Slice thickness for filtering (float)
- **Scale Factor**: Image scaling for thumbnails (int, default: 4)

### Display Parameters
- **Window Width**: Contrast range (adjustable by 100)
- **Window Center**: Brightness level (adjustable by 100)

---

## Error Messages and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| "Invalid folder path." | Directory doesn't exist | Check path spelling and permissions |
| "No se encontraron archivos DICOM válidos" | No valid DICOM files | Verify .dcm files in directory |
| Empty thumbnail grid | Missing pixel data | Check DICOM file integrity |
| Navigation not working | Wrong figure focus | Click on image first |

---

## Tips and Best Practices

### Performance
- Use scale_factor=4 for thumbnails to balance quality and speed
- Close matplotlib windows when done to free memory
- Process large datasets in batches

### File Organization
- Organize DICOM files in patient/study folder structure
- Use consistent naming conventions
- Keep .dcm extensions for all DICOM files

### Troubleshooting
- Check file permissions for read access
- Verify DICOM file integrity with metadata viewer
- Use relative paths when possible for portability

---

## Installation Quick Setup

### Requirements
```bash
pip install pydicom matplotlib pillow numpy
```

### Optional Dependencies
```bash
pip install scipy          # Advanced image processing
pip install opencv-python  # Computer vision features
```

### Quick Test
```python
# Test basic functionality
import pydicom
print("pydicom version:", pydicom.__version__)

import matplotlib
print("matplotlib version:", matplotlib.__version__)
```

---

## Configuration Tips

### Path Configuration
```python
# Recommended: Use configuration file
import json

config = {
    "default_data_path": "/medical/data",
    "scale_factor": 4,
    "window_step": 100
}

with open('config.json', 'w') as f:
    json.dump(config, f)
```

### Display Settings
```python
# Custom window/level defaults
DEFAULT_WINDOW_WIDTH = 400
DEFAULT_WINDOW_CENTER = 200
```

---

## Integration Examples

### Custom Processing Pipeline
```python
from uniqueSeries import find_unique_series_numbers_and_thicknesses
from previewStudies import increase_contrast
import pydicom

def process_study(folder_path):
    # Analyze studies
    series_data = find_unique_series_numbers_and_thicknesses(folder_path)
    
    # Process each series
    for series_num, data in series_data.items():
        print(f"Processing series {series_num}")
        
        # Apply custom processing
        for file_name in data.get('files', []):
            ds = pydicom.dcmread(os.path.join(folder_path, file_name))
            enhanced = increase_contrast(ds.pixel_array)
            # Save or display enhanced image
```

### Batch Processing
```python
def batch_process_patients(root_path):
    for patient_folder in os.listdir(root_path):
        patient_path = os.path.join(root_path, patient_folder)
        if os.path.isdir(patient_path):
            print(f"Processing patient: {patient_folder}")
            process_study(patient_path)
```