import os
import tkinter as tk
from tkinter import Button
from studyInterface import show_series_data
from DICOMVIEWER.uniqueSeries import find_unique_series_numbers_and_thicknesses, show_dicom_study

def show_series_folders(folder_path, series_data):
    root = tk.Tk()
    root.title("Pacientes")
    root.geometry("426x240")  # Establecer tamaño de la ventana

    for folder_name in series_data:
        button = Button(root, text="Paciente " + folder_name, width=50, height=2, command=lambda folder_name=folder_name: show_studies_in_folder(folder_path, folder_name))
        button.pack(fill=tk.BOTH, expand=True)  # Rellenar horizontalmente y expandir
    root.mainloop()

def show_studies_in_folder(root_folder, folder_name):
    folder_path = os.path.join(root_folder, folder_name)
    series_data = find_unique_series_numbers_and_thicknesses(folder_path)
    show_series_data(folder_path, series_data)

def main():
    folder_path = r'D:\TFG\estudios_ct'
    if not os.path.isdir(folder_path):
        print("Invalid folder path.")
        return

    folder_names = [name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]
    show_series_folders(folder_path, folder_names)

if __name__ == "__main__":
    main()
