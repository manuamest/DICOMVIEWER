import tkinter as tk
from tkinter import Button
from studies import find_unique_series_numbers_and_thicknesses, show_dicom_study

def show_series_data(folder_path, series_data):
    
    root = tk.Tk()
    root.title("DICOM Studies")
    
    for series_number, data in series_data.items():
        # Iterar sobre los grosores
        for thickness in data['thicknesses']:
            button_text = f"Series Number: {series_number}, Thickness: {thickness}"
            button = Button(root, text=button_text, command=lambda series_number=series_number, thickness=thickness: show_dicom_study(folder_path, series_number, thickness))
            button.pack()
        
        # Mostrar los estudios sin grosor solo una vez por serie
        if data['no_thickness']:
            button_text = f"Series Number: {series_number}, No Thickness"
            button = Button(root, text=button_text, command=lambda series_number=series_number, thickness=None: show_dicom_study(folder_path, series_number, thickness))
            button.pack()
    
    root.mainloop()

def main():
    folder_path = r'D:\TFG\estudios_ct\1'
    series_data = find_unique_series_numbers_and_thicknesses(folder_path)
    
    show_series_data(folder_path, series_data)

if __name__ == "__main__":
    main()
