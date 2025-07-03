# DICOM Viewer System - Component Architecture Documentation

## System Overview

The DICOM Visualization System is architected as a modular, event-driven application with clear separation of concerns. The system follows a layered architecture pattern with distinct presentation, business logic, and data access layers.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                 Presentation Layer                       │
├─────────────────────────────────────────────────────────┤
│  pacientInterface  │  previewStudies  │  studyInterface │
│  (Patient Select)  │  (Thumbnails)    │  (Text List)    │
└─────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────┐
│                 Business Logic Layer                    │
├─────────────────────────────────────────────────────────┤
│           DicomViewer (Core Viewer)                     │
│           uniqueSeries (Data Processing)                │
└─────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────┐
│                 Data Access Layer                       │
├─────────────────────────────────────────────────────────┤
│           pydicom (DICOM File Reading)                  │
│           File System Operations                        │
└─────────────────────────────────────────────────────────┘
```

## Core Components

### 1. DicomViewer (Core Engine)

**File:** `dicom_viewer.py`
**Role:** Central image viewing and manipulation engine
**Responsibilities:**
- DICOM image rendering and display
- Window/Level adjustments
- Interactive navigation (keyboard/mouse)
- Study organization and filtering

**Design Patterns:**
- **Singleton Pattern**: Class-level instances list for event management
- **Observer Pattern**: Event-driven interaction handling
- **State Pattern**: Navigation state management

**Key Features:**
- Multi-study support with thickness filtering
- Real-time window/level adjustment
- Event-driven navigation system
- Matplotlib integration for professional image display

### 2. Patient Interface (Entry Point)

**File:** `pacientInterface.py`
**Role:** Application entry point and patient selection
**Responsibilities:**
- Initial application launch
- Patient folder discovery
- Navigation to study interfaces

**Design Patterns:**
- **Facade Pattern**: Simplifies access to complex study selection
- **Command Pattern**: Button actions encapsulated as commands

**Integration Points:**
- Connects to `previewStudies` for thumbnail interface
- Validates file system structure
- Provides error handling for invalid paths

### 3. Preview Studies (Thumbnail Interface)

**File:** `previewStudies.py`
**Role:** Visual study selection with thumbnail previews
**Responsibilities:**
- DICOM thumbnail generation
- Dynamic grid layout management
- Contrast enhancement for visibility
- Study metadata display

**Design Patterns:**
- **Factory Pattern**: Dynamic button creation
- **Strategy Pattern**: Different contrast enhancement strategies
- **Composite Pattern**: Complex UI composition

**Advanced Features:**
- Adaptive grid layout (5-8 columns based on study count)
- Memory-efficient image scaling
- Reference management to prevent garbage collection
- Responsive design for different study counts

### 4. Study Interface (Text-Based Selection)

**File:** `studyInterface.py`
**Role:** Alternative text-based study selection
**Responsibilities:**
- Text-based study representation
- Simplified study selection
- Consistent layout management

**Design Patterns:**
- **Template Method Pattern**: Consistent button creation
- **Adapter Pattern**: Adapts study data for display

### 5. Unique Series (Data Processing)

**File:** `uniqueSeries.py`
**Role:** DICOM data analysis and organization
**Responsibilities:**
- DICOM file scanning and analysis
- Series and thickness extraction
- Study metadata organization
- Viewer instance management

**Design Patterns:**
- **Builder Pattern**: Complex study data structure construction
- **Repository Pattern**: Data access abstraction

**Data Structures:**
```python
series_data = {
    'series_number': {
        'thicknesses': set([float, ...]),
        'no_thickness': [str, ...],
        'series_description': str
    }
}
```

## Data Flow Architecture

### 1. Application Startup Flow

```
main.py → pacientInterface() → show_series_folders() → GUI Display
```

**Process:**
1. Application entry point defines root data path
2. Patient interface scans for patient directories
3. GUI displays patient selection buttons
4. User selection triggers study interface

### 2. Study Selection Flow

```
Patient Selection → show_studies_in_folder() → previewStudies() → show_series_data()
```

**Process:**
1. Patient folder path construction
2. DICOM file discovery and analysis
3. Series data organization
4. Thumbnail generation and display

### 3. Viewer Launch Flow

```
Study Selection → show_dicom_study() → DicomViewer() → matplotlib Display
```

**Process:**
1. Study parameters extraction
2. DicomViewer instance creation
3. Study loading and organization
4. Interactive viewer display

### 4. Image Navigation Flow

```
User Input → Event Handler → Navigation Method → Display Update
```

**Event Types:**
- **Keyboard Events**: Arrow keys, window/level shortcuts
- **Mouse Events**: Scroll wheel navigation
- **Programmatic**: Method calls for automation

## Integration Patterns

### 1. File System Integration

**Pattern:** Repository Pattern with Direct File Access

```python
# File discovery pattern
for file_name in os.listdir(folder_path):
    if file_name.endswith('.dcm'):
        # Process DICOM file
```

**Benefits:**
- Direct file system access for performance
- Simple folder-based organization
- No database dependencies

### 2. GUI Framework Integration

**Pattern:** Multiple GUI Toolkit Support

**Tkinter Integration:**
- Patient and study selection interfaces
- Button-based navigation
- Grid and pack layout managers

**Matplotlib Integration:**
- Professional image display
- Interactive event handling
- Zooming and panning capabilities

### 3. DICOM Library Integration

**Pattern:** Adapter Pattern with pydicom

```python
# DICOM reading abstraction
ds = pydicom.dcmread(file_path)
series_number = str(ds.get("SeriesNumber"))
thickness = ds.get("SliceThickness")
```

**Features:**
- Robust metadata extraction
- Pixel data access
- DICOM standard compliance

## Error Handling Strategy

### 1. Graceful Degradation

**Invalid Files:**
- Skip non-DICOM files silently
- Display placeholder for missing pixel data
- Continue processing remaining valid files

**Missing Metadata:**
- Default values for missing window/level
- Handle missing thickness gracefully
- Provide fallback descriptions

### 2. User Feedback

**Path Validation:**
```python
if not os.path.isdir(folder_path):
    print("Invalid folder path.")
    return
```

**Empty Study Handling:**
```python
if not self.studies:
    plt.text(0.5, 0.5, 'No se encontraron archivos DICOM válidos')
```

### 3. Exception Safety

**Resource Management:**
- Proper figure cleanup
- Memory efficient image handling
- Event handler registration/deregistration

## Performance Considerations

### 1. Image Processing Optimization

**Thumbnail Generation:**
- Configurable scale factors (default: 4x reduction)
- Memory-efficient PIL/Pillow operations
- Lazy loading of full-resolution images

**Contrast Enhancement:**
```python
# Optimized contrast enhancement
image = (image - np.min(image)) / (np.max(image) - np.min(image))
image = np.power(image, 0.5)  # Gamma correction
```

### 2. Memory Management

**Image Reference Management:**
```python
# Prevent garbage collection of displayed images
image_references = []
image_references.append(img)
```

**Lazy Loading:**
- Load images only when needed
- Cache frequently accessed studies
- Cleanup unused resources

### 3. File System Optimization

**Directory Scanning:**
- Single-pass file discovery
- Extension-based filtering
- Metadata caching where appropriate

## Extensibility Points

### 1. Custom Viewers

**Interface Contract:**
```python
class CustomViewer:
    def __init__(self, folder_path, series_number, thickness):
        pass
    
    def show_dicom(self, image=None):
        pass
    
    def next_dicom(self):
        pass
    
    def prev_dicom(self):
        pass
```

### 2. Additional GUI Interfaces

**Study Selection Extensions:**
- Custom preview layouts
- Alternative navigation patterns
- Enhanced metadata display

### 3. Image Processing Plugins

**Contrast Enhancement:**
```python
def custom_contrast_enhancement(image):
    # Custom algorithm implementation
    return enhanced_image
```

**Filter Integration:**
- Noise reduction filters
- Edge enhancement
- Custom windowing algorithms

## Configuration Management

### 1. Path Configuration

**Current Implementation:**
- Hardcoded paths in individual modules
- Direct path specification in main entry points

**Recommended Improvements:**
```python
# Configuration file approach
config = {
    'default_data_path': '/medical/data',
    'scale_factor': 4,
    'window_adjustment_step': 100
}
```

### 2. UI Configuration

**Layout Parameters:**
- Button sizes and spacing
- Grid column calculations
- Window dimensions

**Display Settings:**
- Default window/level values
- Color map selections
- Font and label configurations

## Security Considerations

### 1. File Access Security

**Path Validation:**
- Prevent directory traversal attacks
- Validate file extensions
- Check file permissions

**DICOM Data Protection:**
- Handle patient information carefully
- Implement access logging
- Consider data anonymization

### 2. GUI Security

**Input Validation:**
- Sanitize file paths
- Validate user inputs
- Prevent injection attacks

## Testing Strategy

### 1. Unit Testing Approach

**Core Components:**
```python
# Example test structure
class TestDicomViewer(unittest.TestCase):
    def test_load_studies(self):
        # Test study loading functionality
        pass
    
    def test_navigation(self):
        # Test image navigation
        pass
    
    def test_window_level_adjustment(self):
        # Test window/level changes
        pass
```

### 2. Integration Testing

**GUI Integration:**
- Test interface interactions
- Validate data flow between components
- Check event handling

**File System Integration:**
- Test with various DICOM file structures
- Validate error handling for corrupted files
- Check performance with large datasets

### 3. User Acceptance Testing

**Workflow Testing:**
- Complete patient-to-viewer workflows
- Navigation and interaction testing
- Performance validation with real datasets

## Deployment Considerations

### 1. Dependencies Management

**Required Libraries:**
```bash
# Core dependencies
pip install pydicom matplotlib pillow numpy

# Optional enhancements
pip install scipy  # Advanced image processing
pip install opencv-python  # Computer vision features
```

### 2. Platform Compatibility

**Cross-Platform Support:**
- Windows path handling (backslashes)
- Linux/Mac compatibility
- Tkinter availability across platforms

### 3. Performance Optimization

**Production Deployment:**
- Compile Python modules for performance
- Optimize image loading pipelines
- Consider memory usage for large datasets

## Future Enhancement Opportunities

### 1. Advanced Features

**3D Visualization:**
- Volume rendering capabilities
- Multi-planar reconstruction
- 3D navigation tools

**Measurement Tools:**
- Distance and area measurements
- Annotation capabilities
- Report generation

### 2. Collaborative Features

**Multi-User Support:**
- Shared viewing sessions
- Annotation sharing
- User preference management

**Integration APIs:**
- PACS integration
- HL7 FHIR support
- Cloud storage connectivity

### 3. Performance Enhancements

**Caching Systems:**
- Intelligent image caching
- Metadata indexing
- Predictive loading

**Parallel Processing:**
- Multi-threaded image loading
- Background processing
- GPU acceleration for image operations