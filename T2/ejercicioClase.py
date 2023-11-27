import os
import time
import subprocess
import psutil
from multiprocessing import Process, Lock

def listar_procesos():
    print("Listando procesos:")
    for proceso in psutil.process_iter(['pid', 'name', 'username']):
        print(proceso.info)

def proceso_1(lock, nuevo_proceso_1):
    pid = os.getpid()
    print(f"Proceso 1 (PID {pid}) creado.")

    # Hacer algo durante 10 segundos
    time.sleep(10)

    # Matar al proceso 2
    with lock:
        try:
            nuevo_proceso_1.terminate()
            print("Proceso 2 terminado.")
        except AttributeError:
            print("Proceso 2 no encontrado.")

    # Crear un nuevo proceso 1
    print("Creando un nuevo proceso 1...")
    nuevo_proceso_1 = Process(target=proceso_1, args=(lock, nuevo_proceso_1))
    nuevo_proceso_1.start()
    nuevo_proceso_1.join()

def proceso_2(lock, nuevo_proceso_1):
    time.sleep(5)

    # Cambiar la prioridad del primer proceso
    with lock:
        try:
            proceso_1_pid = nuevo_proceso_1.pid
            proceso_1 = psutil.Process(proceso_1_pid)
            proceso_1.nice(5)  # Cambiar la prioridad a 5
            print(f"Prioridad del Proceso 1 cambiada a 5.")
        except psutil.NoSuchProcess:
            print("Proceso 1 no encontrado.")

    # Lanzar el comando ping a la web de Google
    print("Lanzando el comando ping a la web de Google...")
    subprocess.run(["ping", "-c", "5", "www.google.com"])

if name == "main":
    lock = Lock()  # Crear un objeto 'Lock' para sincronización

    # Crear proceso 1
    proceso_1_pid = os.getpid()
    p1 = Process(target=proceso_1, args=(lock, None))
    p1.start()

    # Crear proceso 2
    p2 = Process(target=proceso_2, args=(lock, p1))
    p2.start()

    # Esperar a que ambos procesos terminen
    p1.join()
    p2.join()

    # Mostrar información sobre los procesos usando psutil
    listar_procesos()