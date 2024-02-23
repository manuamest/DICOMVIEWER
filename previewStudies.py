import tkinter as tk
from tkinter import Button
import pydicom
from PIL import Image, ImageTk
import os
from uniqueSeries import show_dicom_study, find_unique_series_numbers_and_thicknesses
import numpy as np

# Lista para almacenar las referencias de las imágenes
image_references = []

def load_dicom_image(file_path, scale_factor=4):
    ds = pydicom.dcmread(file_path)
    if 'PixelData' in ds:
        img = ds.pixel_array

        # Aplicar aumento de contraste solo si el grosor está definido
        if ds.get('SliceThickness') is not None:
            img = increase_contrast(img)

        img = Image.fromarray(img.astype('uint8'))
        new_width = img.width // scale_factor
        new_height = img.height // scale_factor
        img = img.resize((new_width, new_height))
        img = ImageTk.PhotoImage(img)
        return img, new_width, new_height
    else:
        return None, 0, 0

def increase_contrast(image):
    # Normalizar la imagen entre 0 y 1
    image = (image - np.min(image)) / (np.max(image) - np.min(image))
    # Aplicar aumento de contraste
    image = np.power(image, 0.5)
    # Escalar nuevamente a 0-255
    image = (image * 255).astype(np.uint8)
    return image

def create_button(folder_path, root, button_text, img_path, series_number, thickness, series_data, row, col, img_list):
    img = load_dicom_image(img_path)
    if img:
        img_list.append(img)
        image_references.append(img)  # Añadir la referencia de la imagen a la lista de referencias
        button = Button(root, text=button_text, image=img[0], compound=tk.TOP, width=img[0].width(), height=img[0].height(),
                        command=lambda series_number=series_number, thickness=thickness, series_data=series_data: show_dicom_study(folder_path, series_number, thickness))
        button.grid(row=row, column=col, padx=5, pady=5)

def show_series_data(folder_path, series_data):
    root = tk.Toplevel()
    root.title("DICOM Studies")
    
    # Contar el total de estudios de thickness
    total_thickness = sum(len(data['thicknesses']) for data in series_data.values())
    total_buttons = len(series_data) + total_thickness

    # Determinar el número de columnas según la cantidad total de botones
    if total_buttons > 35:
        num_columns = 8
    elif total_buttons > 30:
        num_columns = 7
    elif total_buttons > 25:
        num_columns = 6
    else:
        num_columns = 5

    row = 0
    col = 0
    img_paths = []
    img_list = []
    
    for series_number, data in series_data.items():

        for thickness in data['thicknesses']:
            series_description = data['series_description']
            button_text = f"{series_description}\n"
            series_image_paths = [image_path for image_path, image_thickness in data.get('images_for_series', []) if image_thickness == thickness]
            if series_image_paths:
                file_path = series_image_paths[0]
                img_paths.append(file_path)
                create_button(folder_path, root, button_text, file_path, series_number, thickness, data, row, col, img_list)
            col += 1
            if col == num_columns:
                col = 0
                row += 1
        # Verificar si hay archivos sin thickness para esta serie
        if data['no_thickness']:
            series_description = data['series_description']
            no_thickness_file_path = os.path.join(folder_path, data['no_thickness'][0])  # Tomar solo el primer archivo sin thickness
            img_paths.append(no_thickness_file_path)
            create_button(folder_path, root, f"{series_description}\n", no_thickness_file_path, series_number, None, data, row, col, img_list)
            col += 1
            if col == num_columns:
                col = 0
                row += 1
        
    root.mainloop()
    return img_paths



def previewStudies(folder_path = r'D:\TFG\estudios_ct\1'):
    series_data = find_unique_series_numbers_and_thicknesses(folder_path)
    
    for series_number, data in series_data.items():
        images_for_series = []
        
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.dcm'):
                file_path = os.path.join(folder_path, file_name)
                ds = pydicom.dcmread(file_path)
                
                if str(ds.get("SeriesNumber")) == series_number:
                    thickness = ds.get("SliceThickness")
                    
                    if thickness in data['thicknesses'] or (thickness is None and not data['thicknesses']):
                        images_for_series.append((file_path, thickness))
        
        data['images_for_series'] = images_for_series
    
    show_series_data(folder_path, series_data)

if __name__ == "__main__":
    folder_path = r'D:\TFG\estudios_ct\1'
    previewStudies(folder_path)
