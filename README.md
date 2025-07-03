# DICOM Visualization System

A Python-based DICOM file visualization and manipulation system designed for desktop environments.

## 📖 Documentation

The main documentation has been moved to the `docs/` folder for better organization:

- **[Main Documentation](docs/README.md)** - Complete project documentation
- **[Project Structure](docs/PROJECT_STRUCTURE.md)** - Understanding the new organization
- **[API Documentation](docs/API_DOCUMENTATION.md)** - API reference
- **[Quick Reference](docs/QUICK_REFERENCE.md)** - Quick start guide

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python scripts/main.py [path_to_dicom_folder]

# Or using the package
python -m dicom_viewer [path_to_dicom_folder]
```

## 📁 Project Structure

This project has been reorganized for better maintainability:

```
dicom-viewer-python/
├── src/dicom_viewer/    # Main package source code
├── docs/                # Documentation
├── scripts/             # Entry point scripts
├── tests/               # Test files
└── requirements.txt     # Dependencies
```

For detailed information about the project structure, see [PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md).

## 🔧 Development

To set up for development:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
```

---

*For complete documentation and usage instructions, please refer to the files in the `docs/` directory.*