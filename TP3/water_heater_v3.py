import matplotlib.pyplot as plt
import numpy as np

class Calentador:
    def __init__(self, temperatura_inicial, masa, tiempo, voltaje):
        self.temperatura = temperatura_inicial
        self.masa = masa
        self.set_tiempo(tiempo)
        self.constante_calor = 4.18  # constante de calor específico del agua
        self.voltaje = voltaje

    def get_temperatura(self):
        return self.temperatura
    
    def set_temperatura(self, temperatura):
        self.temperatura = temperatura
    
    def get_masa(self):
        return self.masa
    
    def set_masa(self, masa):
        self.masa = masa

    def get_tiempo(self):
        return self.tiempo
    
    def set_tiempo(self, tiempo):
        if tiempo >= 0:
            self.tiempo = tiempo
        else:
            print("El tiempo debe ser positivo y en segundos")
    
    def get_voltaje(self):
        return self.voltaje
    
    def set_voltaje(self, voltaje):
        self.voltaje = voltaje

    def calculo_delta_temp(self):
        delta_t = 100 - self.temperatura
        calor = self.constante_calor * self.masa * delta_t
        potencia = calor / self.tiempo
        # corriente = potencia / self.voltaje

        # Resistencia
        # resistencia = self.voltaje / corriente

        nuevo_delta = potencia / ((self.masa / 1000) * self.constante_calor * 1000)
        return nuevo_delta
    
    def graficar(self, nuevo_delta):
        tiempo = self.tiempo
        y = [nuevo_delta * i for i in range(1, tiempo + 1)]
        x = np.arange(1, tiempo + 1)
        slope, intercept = np.polyfit(x, y, 1)
        y_line = slope * x + intercept

        # muestro el gráfico
        plt.plot(x, y_line, 'b-')
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Delta de Temperatura')
        plt.title('Variación de Temperatura con el Tiempo')
        plt.grid(True)
        plt.show()

    def calcular_perdida_calor(self, coeficiente_conductividad, superficie_total, espesor_pared):
        perdida_calor = coeficiente_conductividad * superficie_total * self.temperatura / espesor_pared
        return perdida_calor


calentador1 = Calentador(30, 1000, 300, 220)

# Especificaciones del diseño del dispositivo
coeficiente_conductividad = 2.1  # en Watts/metro Kelvin
superficie_total = 1  # en metros cuadrados
espesor_pared = 0.001  # en metros

# Calcular la pérdida de calor
perdida_calor = calentador1.calcular_perdida_calor(coeficiente_conductividad, superficie_total, espesor_pared)
print("Pérdida de calor del dispositivo:", perdida_calor, "Watts/grado Kelvin")