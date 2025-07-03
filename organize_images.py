#!/usr/bin/env python3
"""
Image Organization Utility
Automatically moves image files to the images/ directory
"""

import os
import shutil
import glob
from pathlib import Path

def organize_images():
    """Move all image files to the images directory"""
    
    # Image file extensions to look for
    image_extensions = [
        '*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', 
        '*.tiff', '*.tif', '*.svg', '*.webp', '*.ico'
    ]
    
    # Create images directory if it doesn't exist
    images_dir = Path('images')
    images_dir.mkdir(exist_ok=True)
    
    moved_files = []
    
    # Search for image files in current directory (excluding subdirectories)
    for extension in image_extensions:
        for file_path in glob.glob(extension, recursive=False):
            if os.path.isfile(file_path):
                filename = os.path.basename(file_path)
                destination = images_dir / filename
                
                # Handle duplicate filenames
                counter = 1
                original_destination = destination
                while destination.exists():
                    name_part = original_destination.stem
                    ext_part = original_destination.suffix
                    destination = images_dir / f"{name_part}_{counter}{ext_part}"
                    counter += 1
                
                try:
                    shutil.move(file_path, destination)
                    moved_files.append((file_path, destination))
                    print(f"Moved: {file_path} -> {destination}")
                except Exception as e:
                    print(f"Error moving {file_path}: {e}")
    
    if moved_files:
        print(f"\nSuccessfully organized {len(moved_files)} image files into the images/ directory.")
    else:
        print("No image files found to organize.")
    
    return moved_files

if __name__ == "__main__":
    organize_images()