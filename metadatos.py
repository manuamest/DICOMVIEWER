import pydicom

# Ruta al archivo DICOM
file_path = "D:\\TFG\\estudios_ct\\1\\1.2.826.0.1.3680043.2.135.738231.47542451.7.1706184668.15.30.dcm"

# Cargar el archivo DICOM
ds = pydicom.dcmread(file_path)

# Mostrar los metadatos
print(ds)
