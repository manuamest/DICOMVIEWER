import os
import pydicom
import matplotlib.pyplot as plt

class DicomViewer:
    instances = []

    def __init__(self, folder_path, series_number, thickness, fig=None):
        self.folder_path = folder_path
        self.series_number = series_number
        self.thickness = thickness
        self.studies = self.load_studies()
        self.current_study_index = 0
        self.current_dicom_index = 0
        if fig is None:
            self.fig = plt.figure()
        else:
            self.fig = fig
        self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        self.instances.append(self)

    def load_studies(self):
        studies = []
        for file_name in os.listdir(self.folder_path):
            if file_name.endswith('.dcm'):
                file_path = os.path.join(self.folder_path, file_name)
                ds = pydicom.dcmread(file_path)
                series_number = str(ds.get("SeriesNumber"))
                thickness = ds.get("SliceThickness")
                if series_number == self.series_number and (thickness == self.thickness or thickness is None):
                    if hasattr(ds, 'WindowWidth') and isinstance(ds.WindowWidth, pydicom.multival.MultiValue) and hasattr(ds, 'WindowCenter') and isinstance(ds.WindowCenter, pydicom.multival.MultiValue):
                        window = float(ds.WindowWidth[0])
                        center = float(ds.WindowCenter[0])
                    elif hasattr(ds, 'WindowWidth') and hasattr(ds, 'WindowCenter'):
                        window = float(ds.WindowWidth)
                        center = float(ds.WindowCenter)
                    else:
                        window = 255
                        center = 127.5
                    if not any(study["thickness"] == thickness for study in studies):
                        studies.append({"thickness": thickness, "files": [file_name], "window_width": window, "window_center": center})
                    else:
                        for study in studies:
                            if study["thickness"] == thickness:
                                study["files"].append(file_name)
                                study["window_width"] = window
                                study["window_center"] = center
                                break
        for study in studies:
            study_files = study["files"]
            study_files.sort(key=lambda x: int(pydicom.dcmread(os.path.join(self.folder_path, x)).get("InstanceNumber")))
            study["files"] = study_files
        return studies

    def load_dicom(self, file_name):
        file_path = os.path.join(self.folder_path, file_name)
        ds = pydicom.dcmread(file_path)
        return ds.pixel_array

    def show_dicom(self, image=None):
        plt.clf()
        if not self.studies:
            plt.text(0.5, 0.5, 'No se encontraron archivos DICOM válidos', ha='center', va='center')
            plt.draw()
            return
        current_study = self.studies[self.current_study_index]
        current_file_name = current_study["files"][self.current_dicom_index]
        if image is None:
            image = self.load_dicom(current_file_name)

        window_width = current_study["window_width"]
        window_center = current_study["window_center"]

        plt.imshow(image, cmap=plt.cm.gray, vmin=(window_center - 0.5 - (window_width - 1) / 2), vmax=(window_center - 0.5 + (window_width - 1) / 2))
        plt.axis('off')
        thickness = "{:.2f}".format(current_study["thickness"]) if current_study["thickness"] is not None else "Unknown"
        title = f'DICOM {self.current_dicom_index + 1}/{len(current_study["files"])} del estudio {self.series_number} con thickness {thickness}'
        plt.title(f'{title}\nWindow/Level: {window_width}/{window_center}')
        plt.draw()

    def next_dicom(self):
        current_study = self.studies[self.current_study_index]
        if self.current_dicom_index + 1 < len(current_study["files"]):
            self.current_dicom_index += 1
        self.show_dicom()

    def prev_dicom(self):
        current_study = self.studies[self.current_study_index]
        if self.current_dicom_index - 1 >= 0:
            self.current_dicom_index -= 1
        self.show_dicom()

    def increase_window_width(self):
        for study in self.studies:
            study["window_width"] += 100
        self.show_dicom()

    def decrease_window_width(self):
        for study in self.studies:
            if study["window_width"] - 100 >= study["window_center"]:
                study["window_width"] -= 100
        self.show_dicom()

    def increase_window_center(self):
        for study in self.studies:
            study["window_center"] += 100
        self.show_dicom()

    def decrease_window_center(self):
        for study in self.studies:
            if study["window_center"] - 100 >= 0:
                study["window_center"] -= 100
        self.show_dicom()

    def on_scroll(self, event):
        current_fig = plt.gcf()
        if current_fig == self.fig:
            if event.button == 'down':
                self.next_dicom()
            elif event.button == 'up':
                self.prev_dicom()

    def on_key(self, event):
        current_fig = plt.gcf()
        if current_fig == self.fig:
            if event.key == 'down':
                self.next_dicom()
            elif event.key == 'up':
                self.prev_dicom()
            elif event.key == 'i':
                self.increase_window_width()
            elif event.key == 'k':
                self.decrease_window_width()
            elif event.key == 'j':
                self.increase_window_center()
            elif event.key == 'l':
                self.decrease_window_center()

def main():
    folder_path = r'D:\TFG\estudios_ct\1'
    viewer = DicomViewer(folder_path, '301', '0.3')
    viewer.show_dicom()
    plt.show()

if __name__ == "__main__":
    main()
