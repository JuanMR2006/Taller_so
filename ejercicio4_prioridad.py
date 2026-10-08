import multiprocessing
import sys
import time

import psutil

ITERACIONES = 30_000_000


def calculo_pesado():
    """Cálculo matemático pesado: suma de raíces cuadradas."""
    total = 0.0
    for i in range(ITERACIONES):
        total += (i ** 0.5) * 2.5
    return total


def trabajador(nombre, prioridad, resultados):
    proceso = psutil.Process()
    proceso.cpu_affinity([0])      # mismo núcleo para que compitan
    proceso.nice(prioridad)        # cambia la prioridad en el SO

    inicio = time.perf_counter()
    calculo_pesado()
    duracion = time.perf_counter() - inicio

    resultados.append((nombre, duracion))
    print(f"{nombre} terminó en {duracion:.2f} s")


def main():
    # Prioridades de Windows (psutil)
    baja = psutil.IDLE_PRIORITY_CLASS
    alta = psutil.HIGH_PRIORITY_CLASS   # ver nota abajo sobre Tiempo Real

    with multiprocessing.Manager() as manager:
        resultados = manager.list()

        p1 = multiprocessing.Process(target=trabajador, args=("Proceso BAJA", baja, resultados))
        p2 = multiprocessing.Process(target=trabajador, args=("Proceso ALTA", alta, resultados))

        p1.start()
        p2.start()
        p1.join()
        p2.join()

        print("\n--- Orden de llegada ---")
        for pos, (nombre, dur) in enumerate(sorted(resultados, key=lambda r: r[1]), 1):
            print(f"{pos}. {nombre}: {dur:.2f} s")


if __name__ == "__main__":
    if sys.platform != "win32":
        print("Este script usa las clases de prioridad de Windows.")
    main()