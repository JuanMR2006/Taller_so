import time
from datetime import datetime

import psutil

UMBRAL_RAM = 80          # % de RAM que dispara la alerta
INTERVALO = 1            # segundos entre cada medición
ARCHIVO_LOG = "alertas_ram.txt"


def guardar_alerta(ram, cpu):
    """Escribe una línea en el log cuando la RAM supera el umbral."""
    marca = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ARCHIVO_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{marca}] ALERTA: RAM al {ram}% (CPU {cpu}%)\n")


def main():
    print("Vigilante de recursos iniciado. Ctrl + C para detener.\n")
    try:
        while True:
            cpu = psutil.cpu_percent(interval=None)
            ram = psutil.virtual_memory().percent

            estado = "ALERTA" if ram > UMBRAL_RAM else "OK"
            print(f"CPU: {cpu:5.1f}% | RAM: {ram:5.1f}% | {estado}")

            if ram > UMBRAL_RAM:
                guardar_alerta(ram, cpu)

            time.sleep(INTERVALO)
    except KeyboardInterrupt:
        print("\nVigilante detenido.")


if __name__ == "__main__":
    main()