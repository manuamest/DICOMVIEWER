"""
Image processing utilities for DICOM files.

Contains utility functions for loading, processing, and enhancing DICOM images.
"""

import numpy as np
from PIL import Image
import pydicom


def load_dicom_image(file_path, scale_factor=4):
    """Load and process a DICOM image with optional scaling."""
    dicom_data = pydicom.dcmread(file_path)
    image = dicom_data.pixel_array.astype(float)
    
    # Apply contrast enhancement only if thickness is defined
    if hasattr(dicom_data, 'SliceThickness'):
        if float(dicom_data.SliceThickness) >= 1.0:
            image = increase_contrast(image)
    
    # Normalize and convert to PIL Image
    image = (image - np.min(image)) / (np.max(image) - np.min(image)) * 255
    image = image.astype(np.uint8)
    pil_image = Image.fromarray(image)
    
    # Scale the image
    new_size = (image.shape[1] // scale_factor, image.shape[0] // scale_factor)
    pil_image = pil_image.resize(new_size, Image.LANCZOS)
    
    return pil_image


def increase_contrast(image):
    """
    Increase contrast of the image using histogram stretching.
    
    Args:
        image: Input image as numpy array
        
    Returns:
        Contrast-enhanced image as numpy array
    """
    # Calculate percentiles for contrast stretching
    p2, p98 = np.percentile(image, (2, 98))
    # Stretch the histogram
    image_stretched = np.clip((image - p2) / (p98 - p2) * 255, 0, 255)
    return image_stretched