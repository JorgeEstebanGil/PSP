import threading
import queue
import random
import time

CT = 6
X =4
class Producer(threading.Thread):
    """
    Produces random integers to a list
    """

    def __init__(self, queue, PT):
        """
        Constructor.

        @param integers list of integers
        @param event event synchronization object
        """
        threading.Thread.__init__(self)
        self.queue = queue
        self.PT = PT
    
    def run(self):
        """
        Thread run method. Append random integers to the integers list
        at random time.
        """
        while True:
            for _ in range(15):
                num = random.randint(50, 2000)
                self.queue.put(num)
                print(f"Producido: {num}")
                time.sleep(self.PT) # @PT Producer time


class Consumer(threading.Thread):
    """
    Consumes random integers from a list
    """

    def __init__(self, queue,CT,X):
        """
        Constructor.

        @param integers list of integers
        @param event event synchronization object
        """
        threading.Thread.__init__(self)
        self.queue = queue
        self.CT = CT
        self.X = X
    
    def run(self):
        """
        Thread run method. Consumes integers from list
        """
        while True:
            numeros = []
            for i in range(X):
                numeros.append(self.queue.get())
                print(f"Consumiendo: {numeros[i]}")
            
            suma_cuadrados = sum(x**2 for x in numeros)
            print(f"Consumidos: {numeros}, Suma de cuadrados: {suma_cuadrados}")
            time.sleep(self.CT) #CT Consumer time


# Caso 1:1 
q_1_1 = queue.Queue()
p_1_1 = Producer(q_1_1, PT=2)
c_1_1 = Consumer(q_1_1, CT=6, X=4)

# Caso 5:2 
q_5_2 = queue.Queue()
p_5_2 = Producer(q_5_2, PT=1)
c_5_2 = Consumer(q_5_2, CT=3, X=5)

# Caso 3:10 
q_3_10 = queue.Queue()
p_3_10 = Producer(q_3_10, PT=3)
c_3_10 = Consumer(q_3_10, CT=8, X=2)


# Iniciar los hilos
p_1_1.start()
time.sleep(1)
c_1_1.start()

p_5_2.start()
time.sleep(1)
c_5_2.start()

p_3_10.start()
time.sleep(1)
c_3_10.start()

# Esperar a que los hilos terminen
p_1_1.join()
c_1_1.join()

p_5_2.join()
c_5_2.join()

p_3_10.join()
c_3_10.join()