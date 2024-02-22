import tkinter as tk
from tkinter import Button
import pydicom
from uniqueSeries import find_unique_series_numbers_and_thicknesses, show_dicom_study
from PIL import Image, ImageTk
import os

def load_dicom_image(file_path, scale_factor=4):
    ds = pydicom.dcmread(file_path)
    if 'PixelData' in ds:
        img = ds.pixel_array
        img_min = img.min()
        img_max = img.max()
        img = (img - img_min) / (img_max - img_min) * 255
        img = Image.fromarray(img.astype('uint8'))
        new_width = img.width // scale_factor
        new_height = img.height // scale_factor
        img = img.resize((new_width, new_height))
        img = ImageTk.PhotoImage(img)
        return img, new_width, new_height
    else:
        return None, 0, 0

def create_button(folder_path, root, button_text, img_path, series_number, thickness, series_data, row, col, img_list):
    img = load_dicom_image(img_path)
    if img:
        img_list.append(img)  # Agregar la imagen a la lista para mantener la referencia
        button = Button(root, text=button_text, image=img[0], compound=tk.TOP, width=img[0].width(), height=img[0].height(),
                        command=lambda series_number=series_number, thickness=thickness, series_data=series_data: show_dicom_study(folder_path, series_number, thickness))
        button.grid(row=row, column=col, padx=5, pady=5)

def show_series_data(folder_path, series_data):
    root = tk.Tk()
    root.title("DICOM Studies")
    
    row = 0
    col = 0
    img_paths = []  # Lista para almacenar las rutas de las imágenes
    img_list = []  # Lista para mantener las referencias a las imágenes
    for series_number, data in series_data.items():
        for thickness in data['thicknesses']:
            series_description = data['series_description']
            button_text = f"{series_description}\n"
            file_path = data.get('image_path', None)  # Obtener la ruta de la imagen
            if file_path:
                img_paths.append(file_path)  # Agregar la ruta de la imagen a la lista
                create_button(folder_path, root, button_text, file_path, series_number, thickness, data, row, col, img_list)
            col += 1
            if col == 3:
                col = 0
                row += 1
        if data['no_thickness']:
            series_description = data['series_description']
            button_text = f"{series_description}\n"
            file_path = data.get('image_path', None)  # Obtener la ruta de la imagen
            if file_path:
                img_paths.append(file_path)  # Agregar la ruta de la imagen a la lista
                create_button(folder_path, root, button_text, file_path, series_number, None, data, row, col, img_list)
            col += 1
            if col == 3:
                col = 0
                row += 1
    
    root.mainloop()
    return img_paths

def main():
    folder_path = r'D:\TFG\estudios_ct\1'
    series_data = find_unique_series_numbers_and_thicknesses(folder_path)
    
    for series_number, data in series_data.items():
        # Lista para almacenar las rutas de las imágenes dentro del mismo número de serie y grosor
        images_for_series = []
        
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.dcm'):
                file_path = os.path.join(folder_path, file_name)
                ds = pydicom.dcmread(file_path)
                
                # Comprobar si la imagen pertenece al mismo número de serie y grosor
                if str(ds.get("SeriesNumber")) == series_number:
                    thickness = ds.get("SliceThickness")
                    
                    # Si el grosor coincide con el grosor registrado o si ambos son None
                    if thickness in data['thicknesses'] or (thickness is None and not data['thicknesses']):
                        images_for_series.append((file_path, thickness))
        

            for image_path, thickness in images_for_series:
                data['image_path'] = image_path
                data['thickness'] = thickness
                break


    img_paths = show_series_data(folder_path, series_data)
    return img_paths

if __name__ == "__main__":
    main()
