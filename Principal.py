import os
import shutil
from datetime import datetime

# Función para obtener la fecha de creación del archivo
def obtener_fecha_archivo(archivo):
    timestamp = os.path.getctime(archivo)  # Obtiene la fecha de creación
    return datetime.fromtimestamp(timestamp)

# Función para eliminar carpetas vacías
def eliminar_carpetas_vacias(ruta_principal):
    for carpeta_raiz, subcarpetas, archivos in os.walk(ruta_principal, topdown=False):
        # Si la carpeta está vacía (sin subcarpetas y sin archivos)
        if not subcarpetas and not archivos:
            os.rmdir(carpeta_raiz)  # Elimina la carpeta vacía
            print(f'Carpeta vacía eliminada: {carpeta_raiz}')

# Función para clasificar los archivos
def clasificar_archivos_por_tipo_y_fecha(ruta_origen, ruta_destino):
    for carpeta_raiz, subcarpetas, archivos in os.walk(ruta_origen):
        for archivo in archivos:
            # Obtener la ruta completa del archivo
            ruta_archivo = os.path.join(carpeta_raiz, archivo)
            
            # Obtener la extensión del archivo (por ejemplo, .txt, .jpg)
            extension = os.path.splitext(archivo)[1].lower()
            
            # Definir una carpeta para el tipo de archivo (por extensión)
            if extension in ['.jpeg','.jpg', '.png', '.gif']:
                tipo = 'Imagenes'
            elif extension in ['.txt', '.pdf', '.docx', '.xlsx']:
                tipo = 'Documentos'
            elif extension in ['.mp3', '.wav']:
                tipo = 'Audio'
            elif extension in ['.mp4', '.avi', '.opus']:
                tipo = 'Videos'
            elif extension in ['.apk']:
                tipo = 'Apk'
            elif extension in ['.html']:
                tipo = 'Html'    
            elif extension in ['.zip', '.rar', '.csv']:
                tipo = 'Archivos comprimidos'
            elif extension in ['.psd', 'pptx']:
                tipo = 'Diseño'
            else:
                tipo = 'Otros'

            # Obtener la fecha de creación del archivo
            fecha_modificacion = obtener_fecha_archivo(ruta_archivo)
            anio = fecha_modificacion.strftime('%Y')
            mes = fecha_modificacion.strftime('%m')

            # Crear una nueva ruta en la carpeta de destino, con subcarpetas de tipo y fecha
            nueva_carpeta = os.path.join(ruta_destino, tipo, f'{anio}-{mes}')
            os.makedirs(nueva_carpeta, exist_ok=True)
            
            # Mover el archivo a la nueva carpeta
            nueva_ruta_archivo = os.path.join(nueva_carpeta, archivo)
            shutil.move(ruta_archivo, nueva_ruta_archivo)
            print(f'Archivo {archivo} movido a {nueva_ruta_archivo}')
    
    # Después de mover los archivos, eliminamos las carpetas vacías en la ruta de origen
    eliminar_carpetas_vacias(ruta_origen)

# Ruta principal de origen y destino que deseas organizar
ruta_origen = 'D:\MULTIMEDIA\MUSICA'
ruta_destino = 'D:\MULTIMEDIA\MUSICA\p1'

clasificar_archivos_por_tipo_y_fecha(ruta_origen, ruta_destino)