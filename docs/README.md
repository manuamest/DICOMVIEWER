# DICOM Visualization System in Python
This repository contains the code for a DICOM file visualization and manipulation system developed in Python. Designed for a desktop environment, this system allows users to navigate through a series of images, adjust brightness and contrast (Window/Level), and organize DICOM files by studies and patients.

## Features
- DICOM File Visualization: Displays DICOM images with adjustable brightness and contrast controls.
- Intuitive Navigation: Easily move between instances in a series.
- Patient and Study Organization: Structures files by patient and study, making it easy to search and select.
- Graphical Interface with Tkinter: Provides an interactive and user-friendly interface built with the Tkinter library.
## Installation
1. **Clone the Repository**:
```bash
git clone https://github.com/manuamest/dicom-viewer-python.git
cd dicom-viewer-python
```
2. **Install dependencies**: It's recommended to use a virtual environment.
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
3.**Environment setup**: Ensure the necessary libraries are installed, such as pydicom for DICOM file handling and tkinter for the graphical interface.

## Usage
Run the application:

```bash
python main.py
```
Navigate through studies: Upon launching, the interface shows a list of available DICOM studies in the configured directory. You can select a study and navigate through the images.

Adjust Window/Level: Use keyboard or mouse controls to adjust brightness and contrast of the displayed image, optimizing visibility for specific tissues.

## System UI
Here are some screenshots of the system in action:

1. **Main Interface**: Displaying a DICOM image with adjustable window and level controls.

   ![Main Interface](images/main_interface.png)

2. **Study List**: Interface for selecting and previewing studies.

   ![Study List](images/study_list.png)

3. **Window/Level Adjustment**: Example of level manipulation to enhance visualization.

   ![Window Level Adjustment](images/window_level_adjustment.png)


## Contributions
Contributions are welcome. Please open an issue or pull request for suggestions on improvements or new features.
