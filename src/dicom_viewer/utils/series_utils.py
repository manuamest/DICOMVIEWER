import os
import pydicom
import tkinter as tk
from tkinter import Button
import matplotlib.pyplot as plt
from ..core.dicom_viewer import DicomViewer

def find_unique_series_numbers_and_thicknesses(folder_path):
    series_data = {}
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.dcm'):
            file_path = os.path.join(folder_path, file_name)
            ds = pydicom.dcmread(file_path)
            series_number = str(ds.get("SeriesNumber"))
            thickness = ds.get("SliceThickness")
            series_description = ds.get("SeriesDescription")  # Obtener la descripción de la serie
            if series_number in series_data:
                if thickness is not None:
                    series_data[series_number]['thicknesses'].add(thickness)
                else:
                    series_data[series_number]['no_thickness'].append(file_name)
            else:
                series_data[series_number] = {'thicknesses': set(), 'no_thickness': [], 'series_description': series_description}  # Agregar la descripción de la serie
                if thickness is not None:
                    series_data[series_number]['thicknesses'].add(thickness)
                else:
                    series_data[series_number]['no_thickness'].append(file_name)
    return series_data


def show_dicom_study(folder_path, series_number, thickness):
    fig = plt.figure()
    viewer = DicomViewer(folder_path, series_number, thickness, fig)
    viewer.show_dicom()
    plt.show()

def main():
    folder_path = r'D:\TFG\estudios_ct\1'
    series_data = find_unique_series_numbers_and_thicknesses(folder_path)

    for series_number, data in series_data.items():
        for thickness in data['thicknesses']:
            viewer = DicomViewer(folder_path, series_number, thickness)
            viewer.show_dicom()
            plt.show()

        if data['no_thickness']:
            viewer = DicomViewer(folder_path, series_number, thickness=None)
            for file_name in data['no_thickness']:
                viewer.load_dicom(os.path.join(folder_path, file_name))
            viewer.show_dicom()
            plt.show()

if __name__ == "__main__":
    main()
