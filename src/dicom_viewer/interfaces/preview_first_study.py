import tkinter as tk
from tkinter import Button
import pydicom
from ..utils.series_utils import find_unique_series_numbers_and_thicknesses, show_dicom_study
from PIL import Image, ImageTk
import os

def load_dicom_image(file_path, scale_factor=4):
    ds = pydicom.dcmread(file_path)
    # Asegurarse de que el archivo DICOM tenga datos de imagen
    if 'PixelData' in ds:
        img = ds.pixel_array
        img_min = img.min()
        img_max = img.max()
        img = (img - img_min) / (img_max - img_min) * 255  # Escalar los valores al rango de 0 a 255
        img = Image.fromarray(img.astype('uint8'))
        # Redimensionar la imagen
        new_width = img.width // scale_factor
        new_height = img.height // scale_factor
        img = img.resize((new_width, new_height))
        img = ImageTk.PhotoImage(img)
        return img, new_width, new_height
    else:
        return None, 0, 0



def show_series_data(folder_path, series_data):
    root = tk.Tk()
    root.title("DICOM Studies")
    
    # Mostrar solo la imagen del primer estudio
    series_number, data = next(iter(series_data.items()))
    file_path = data['image_path']
    img, img_width, img_height = load_dicom_image(file_path)
    if img:
        button_text = f"Series Number: {series_number}\nSeries Description: {data['series_description']}"
        button = Button(root, text=button_text, image=img, compound=tk.TOP, width=img_width, height=img_height,
                        command=lambda series_number=series_number, thickness=None, series_data=data: show_dicom_study(folder_path, series_number, thickness))
        button.pack(padx=5, pady=5)
    
    root.mainloop()

def main():
    folder_path = r'D:\TFG\estudios_ct\1'
    series_data = find_unique_series_numbers_and_thicknesses(folder_path)
    
    # Encontrar el primer archivo DICOM y almacenar su ruta en series_data
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.dcm'):
            file_path = os.path.join(folder_path, file_name)
            ds = pydicom.dcmread(file_path)
            series_number = str(ds.get("SeriesNumber"))
            if series_number in series_data:
                series_data[series_number]['image_path'] = file_path
                break
    
    show_series_data(folder_path, series_data)

if __name__ == "__main__":
    main()
