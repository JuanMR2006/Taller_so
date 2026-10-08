import psutil

LIMITE_RAM = 95           # % de RAM del sistema: freno de seguridad
LIMITE_PROCESO_GB = 6     # GB máximos que puede usar este script
LOTE = 200_000            # strings que se agregan en cada vuelta

datos = []
proceso = psutil.Process()
contador = 0

print("Estrés de memoria iniciado. Ctrl + C para detener.\n")

try:
    while True:
        # Strings únicos para que Python no reutilice objetos
        datos.extend(f"cadena_{contador + i}_" + "x" * 100 for i in range(LOTE))
        contador += LOTE

        ram = psutil.virtual_memory().percent
        swap = psutil.swap_memory().percent
        mb_proceso = proceso.memory_info().rss / (1024 * 1024)

        print(f"Strings: {contador:>12,} | RAM: {ram:5.1f}% | "
              f"Swap/Paginación: {swap:5.1f}% | Script: {mb_proceso:8.1f} MB")

        if ram >= LIMITE_RAM or mb_proceso >= LIMITE_PROCESO_GB * 1024:
            print("\nLÍMITE DE SEGURIDAD alcanzado. Deteniendo el llenado.")
            break
except KeyboardInterrupt:
    print("\nDetenido manualmente.")

input("Observa el Administrador de tareas y presiona Enter para liberar la memoria...")
del datos
print("Memoria liberada.")