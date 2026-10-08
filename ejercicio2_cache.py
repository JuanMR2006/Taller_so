import os
import time

ARCHIVO = "archivo_grande.txt"
TAMANO_MB = 100

# La caché: diccionario en RAM  {ruta_del_archivo: contenido}
cache = {}


def crear_archivo_prueba():
    """Genera un archivo de texto de unos 100 MB si no existe."""
    if os.path.exists(ARCHIVO):
        return
    linea = "Linea de prueba para simular un archivo grande del sistema.\n"
    repeticiones = (TAMANO_MB * 1024 * 1024) // len(linea)
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        for _ in range(repeticiones):
            f.write(linea)


def leer_con_cache(ruta):
    """Si el archivo está en la caché lo devuelve de RAM; si no, lo lee del disco."""
    if ruta in cache:
        return cache[ruta], "CACHE (RAM)"
    with open(ruta, "r", encoding="utf-8") as f:
        contenido = f.read()
    cache[ruta] = contenido
    return contenido, "DISCO"


def main():
    crear_archivo_prueba()

    for intento in range(1, 4):
        inicio = time.time()
        contenido, origen = leer_con_cache(ARCHIVO)
        fin = time.time()

        print(f"Lectura {intento}: {origen:12} | "
              f"{len(contenido) / (1024 * 1024):.1f} MB | "
              f"tiempo: {fin - inicio:.6f} s")


if __name__ == "__main__":
    main()