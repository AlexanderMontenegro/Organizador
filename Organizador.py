import os
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

# obtener la fecha de creación 
def obtener_fecha_archivo(archivo):
    timestamp = os.path.getctime(archivo)
    return datetime.fromtimestamp(timestamp)

# eliminar carpetas vacías con manejo de errores
def eliminar_carpetas_vacias(ruta_principal):
    for carpeta_raiz, subcarpetas, archivos in os.walk(ruta_principal, topdown=False):
        try:
            if not subcarpetas and not archivos:
                os.rmdir(carpeta_raiz)
                print(f'Carpeta vacía eliminada: {carpeta_raiz}')
        except PermissionError:
            print(f"No se pudo eliminar {carpeta_raiz}, acceso denegado.")
        except Exception as e:
            print(f"Error al eliminar {carpeta_raiz}: {e}")

# Función para clasificar archivos
def clasificar_archivos_por_tipo_y_fecha(ruta_origen, ruta_destino, barra_progreso, etiqueta_progreso):
    archivos_totales = sum([len(archivos) for _, _, archivos in os.walk(ruta_origen)])
    archivos_procesados = 0

    for carpeta_raiz, subcarpetas, archivos in os.walk(ruta_origen):
        for archivo in archivos:
            if archivo.startswith(".lock"):  # Ignorar archivos en uso
                print(f"Archivo en uso ignorado: {archivo}")
                continue

            ruta_archivo = os.path.join(carpeta_raiz, archivo)
            extension = os.path.splitext(archivo)[1].lower()

            if extension in ['.jpeg', '.jpg', '.png', '.gif']:
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
                tipo = 'Archivos_Comprimidos'
            elif extension in ['.psd', '.pptx']:
                tipo = 'Diseño'
            else:
                tipo = 'Otros'

            fecha_modificacion = obtener_fecha_archivo(ruta_archivo)
            anio = fecha_modificacion.strftime('%Y')
            mes = fecha_modificacion.strftime('%m')

            nueva_carpeta = os.path.join(ruta_destino, tipo, f'{anio}-{mes}')
            try:
                os.makedirs(nueva_carpeta, exist_ok=True)
            except Exception as e:
                print(f"Error al crear carpeta {nueva_carpeta}: {e}")
                continue

            try:
                shutil.move(ruta_archivo, os.path.join(nueva_carpeta, archivo))
                print(f'Archivo {archivo} movido a {nueva_carpeta}')
            except PermissionError:
                print(f"No se pudo mover {archivo}, acceso denegado.")
            except Exception as e:
                print(f"Error al mover {archivo}: {e}")

            archivos_procesados += 1
            progreso = (archivos_procesados / archivos_totales) * 100
            barra_progreso['value'] = progreso
            etiqueta_progreso.config(text=f"Progreso: {int(progreso)}%")
            ventana.update_idletasks()

    eliminar_carpetas_vacias(ruta_origen)
    messagebox.showinfo("Completado", "Los archivos han sido clasificados y organizados.")

# Funciones Usuario
def seleccionar_ruta_origen():
    ruta = filedialog.askdirectory()
    entrada_origen.delete(0, tk.END)
    entrada_origen.insert(0, ruta)

def seleccionar_ruta_destino():
    ruta = filedialog.askdirectory()
    entrada_destino.delete(0, tk.END)
    entrada_destino.insert(0, ruta)

def iniciar_clasificacion():
    ruta_origen = entrada_origen.get()
    ruta_destino = entrada_destino.get()
    if ruta_origen and ruta_destino:
        barra_progreso['value'] = 0
        etiqueta_progreso.config(text="Progreso: 0%")
        clasificar_archivos_por_tipo_y_fecha(ruta_origen, ruta_destino, barra_progreso, etiqueta_progreso)
    else:
        messagebox.showwarning("Advertencia", "Por favor, selecciona ambas rutas.")

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("🚀 Organizador de Archivos ")
ventana.geometry("700x450")
ventana.configure(bg="#121212")

# Estilos
estilo = ttk.Style()
estilo.theme_use("clam")
estilo.configure("TButton",
                 padding=10,
                 font=("Arial Black", 12),
                 background="#FF4500",
                 foreground="white",
                 borderwidth=3,
                 relief="ridge")
estilo.map("TButton",
           background=[("active", "#FF6347")],
           foreground=[("active", "white")])

estilo.configure("TLabel",
                 font=("Courier New", 13, "bold"),
                 background="#121212",
                 foreground="#00FFFF")

estilo.configure("TEntry",
                 font=("Consolas", 12),
                 fieldbackground="#1E1E1E",
                 foreground="white",
                 borderwidth=3,
                 relief="solid",
                 insertcolor="white")

# logo
try:
    imagen = Image.open("Milogo.png")
    imagen = imagen.resize((100, 100), Image.Resampling.LANCZOS)
    imagen_tk = ImageTk.PhotoImage(imagen)
    label_imagen = ttk.Label(ventana, image=imagen_tk, background="#121212")
    label_imagen.grid(row=0, column=0, columnspan=3, pady=10)
except Exception as e:
    print(f"No se pudo cargar la imagen: {e}")

# Accesos
ttk.Label(ventana, text="📂 Ruta de Origen:").grid(row=1, column=0, padx=10, pady=10)
entrada_origen = ttk.Entry(ventana, width=40)
entrada_origen.grid(row=1, column=1, padx=10, pady=10)
ttk.Button(ventana, text="📁 Seleccionar", command=seleccionar_ruta_origen).grid(row=1, column=2, padx=10, pady=10)

ttk.Label(ventana, text="📂 Ruta de Destino:").grid(row=2, column=0, padx=10, pady=10)
entrada_destino = ttk.Entry(ventana, width=40)
entrada_destino.grid(row=2, column=1, padx=10, pady=10)
ttk.Button(ventana, text="📁 Seleccionar", command=seleccionar_ruta_destino).grid(row=2, column=2, padx=10, pady=10)

ttk.Button(ventana, text="🚀 Iniciar Clasificación", command=iniciar_clasificacion).grid(row=3, column=1, pady=20)

# Barra de progreso
barra_progreso = ttk.Progressbar(ventana, orient="horizontal", length=400, mode="determinate")
barra_progreso.grid(row=4, column=0, columnspan=3, pady=10)

# Etiqueta de progreso
etiqueta_progreso = ttk.Label(ventana, text="Progreso: 0%", style="TLabel")
etiqueta_progreso.grid(row=5, column=0, columnspan=3, pady=10)

ventana.grid_propagate(False)

ventana.mainloop()