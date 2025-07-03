import tkinter as tk
from tkinter import Button
from ..utils.series_utils import find_unique_series_numbers_and_thicknesses, show_dicom_study

def show_series_data(folder_path, series_data):
    root = tk.Tk()
    root.title("DICOM Studies")
    
    # Configurar el ancho y alto fijo para los botones
    button_width = 30
    button_height = 5
    
    row = 0
    col = 0
    for series_number, data in series_data.items():
        for thickness in data['thicknesses']:
            # Obtener la descripción de la serie
            series_description = data['series_description']
            # Formatear el grosor con dos decimales
            thickness_formatted = "{:.2f}".format(thickness)
            button_text = f"Series Number: {series_number}, Thickness: {thickness_formatted}\nSeries Description: {series_description}"
            button = Button(root, text=button_text, width=button_width, height=button_height,
                            command=lambda series_number=series_number, thickness=thickness: show_dicom_study(folder_path, series_number, thickness))
            button.grid(row=row, column=col, padx=5, pady=5)  # Utilizando grid en lugar de pack
            col += 1
            # Verificar si se necesita pasar a la siguiente fila
            if col == 3:  # Solo un botón por fila
                col = 0
                row += 1
         
        if data['no_thickness']:
            # Obtener la descripción de la serie
            series_description = data['series_description']
            button_text = f"Series Number: {series_number}, No Thickness\nSeries Description: {series_description}"
            button = Button(root, text=button_text, width=button_width, height=button_height,
                            command=lambda series_number=series_number, thickness=None: show_dicom_study(folder_path, series_number, thickness))
            button.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col == 3:  # Solo un botón por fila
                col = 0
                row += 1
    
    root.mainloop()

def main():
    folder_path = r'D:\TFG\estudios_ct\1'
    series_data = find_unique_series_numbers_and_thicknesses(folder_path)
    
    show_series_data(folder_path, series_data)

if __name__ == "__main__":
    main()
