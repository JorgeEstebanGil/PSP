#Crea dos procesos, y lístalos usando psutil
#El primer proceso estará 10 segundos vivo y matará al otro proceso, finalmente creará un fork de si mismo
#El segundo proceso a los 5 segundos cambiará la prioridad del primer proceso y lanzará el comando ping a la web de google

import psutil
import os
import time
import signal
import subprocess

import psutil
import subprocess
import os
import time
import multiprocessing

def listar_procesos():
    print("Lista de procesos:")
    for proc in psutil.process_iter(['pid', 'name', 'status']):
        print(f"PID: {proc.info['pid']}, Nombre: {proc.info['name']}, Estado: {proc.info['status']}")

def primer_proceso():
    print("Proceso 1 iniciado.", os.getpid())
    time.sleep(10)  # Estará vivo por 10 segundos
    print("Proceso 1 matando al proceso 2.")
    if segundo_pid is not None:  # Check if segundo_pid is not None before killing
        os.kill(segundo_pid, psutil.signal.SIGTERM)  # Matando al segundo proceso
    print("Proceso 1 creando un fork de sí mismo.")
    multiprocessing.Process(target=primer_proceso).start()

def segundo_proceso():
    print("Proceso 2 iniciado.")
    time.sleep(5)  # Espera 5 segundos
    print("Proceso 2 cambiando la prioridad del proceso 1.")
    proc = psutil.Process(primer_pid)
    proc.nice(10)  # Cambiando la prioridad del proceso 1
    print("Proceso 2 lanzando el comando ping a la web de google.")
    subprocess.run(["ping", "www.google.com"])

# Iniciar el primer proceso
primer_pid = os.getpid()
segundo_pid = None

# Guardar el PID del primer proceso para usarlo en el segundo proceso
segundo_process = multiprocessing.Process(target=segundo_proceso)
segundo_process.start()

# Esperar a que el segundo proceso termine
segundo_process.join()

# Listar procesos después de que ambos terminen
listar_procesos()
