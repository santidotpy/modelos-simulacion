import matplotlib.pyplot as plt
import numpy as np
from data_heater import temperatura, masa, tiempo, voltaje

class Calentador:
    def __init__(self, temperatura, masa, tiempo, voltaje):
        self.temperatura = temperatura
        self.masa = masa
        self.tiempo = tiempo
        self.cte = 4.18
        self.voltaje = voltaje

    @property
    def temperatura(self):
        return self._temperatura

    @temperatura.setter
    def temperatura(self, temperatura):
        self._temperatura = temperatura

    @property
    def masa(self):
        return self._masa

    @masa.setter
    def masa(self, masa):
        self._masa = masa

    @property
    def tiempo(self):
        return self._tiempo

    @tiempo.setter
    def tiempo(self, tiempo):
        if tiempo >= 0:
            self._tiempo = tiempo
        else:
            raise ValueError("El tiempo debe ser positivo y en segundos")

    @property
    def voltaje(self):
        return self._voltaje

    @voltaje.setter
    def voltaje(self, voltaje):
        self._voltaje = voltaje

    def calcular_resistencia(self):
        delta_t = 100 - self.temperatura
        q = self.cte * self.masa * delta_t
        p = q / self.tiempo
        i = p / self.voltaje
        r = self.voltaje / i
        return r

    def calcular_delta_temp(self):
        delta_t = 100 - self.temperatura
        q = self.cte * self.masa * delta_t
        p = q / self.tiempo
        nuevo_delta = p / ((self.masa / 1000) * self.cte * 1000)
        return nuevo_delta

    def graficar(self, nuevo_delta):
        x = range(1, self.tiempo + 1)
        y = [nuevo_delta * i for i in x]
        coeficientes = np.polyfit(x, y, 1)
        slope, intercept = coeficientes
        y_line = [slope * i + intercept for i in x]

        plt.plot(x, y_line, 'b-')
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Delta de Temperatura (°C)')
        plt.title('Cambio de Temperatura con el Tiempo')
        plt.grid(True)
        plt.show()

# Creación de la instancia del calentador
calentador1 = Calentador(temperatura, masa, tiempo, voltaje)

# nuevo_delta = calentador1.calcular_delta_temp()
# calentador1.graficar(nuevo_delta)
