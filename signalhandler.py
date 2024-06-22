import signal
import time

# Variable para controlar el estado de CTRL+C
interrupted = False

def signal_handler(signum, frame):
    global interrupted
    if interrupted:
        print("Terminando el programa...")
        exit(0)  # Termina el programa
    else:
        print("CTRL+C detectado. Saltando al siguiente enlace...")
        interrupted = True
        # Restablece la bandera después de un corto tiempo para permitir la detección de doble CTRL+C
        time.sleep(2)
        interrupted = False

# Configura el manejador de señales
signal.signal(signal.SIGINT, signal_handler)