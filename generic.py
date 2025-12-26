from PIL import ImageTk, Image

def leer_imagen(path, size):

    return ImagentK.PhotoImagen(Imagen.open(path).rize(size, Image.Resampling.LANCZOS))
    
def centrar_ventana(ventana,aplicacion_ancho, aplicacion_largo):
    pantalla_largo = ventana.winfo_screenwidth()
    pantalla_ancho = ventana.winfo_screenheight()

    x = int ((pantalla_ancho/2) - (aplicacion_ancho/2))
    y = int ((pantalla_largo/2) - (aplicacion_largo2))
    
    return ventana.geometry(f"{aplicacion_ancho}x{aplicacion_largo}+{x}+{y}")
