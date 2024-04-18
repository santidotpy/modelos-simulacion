import matplotlib.pyplot as plt

class Calentador:
    def __init__(self, temperatura_inicial, masa, tiempo, voltaje):
        self.temperatura_fluido = temperatura_inicial
        self.masa = masa
        self.set_tiempo(tiempo)
        self.constante_calor = 4.18  # Constante de calor específico del agua
        self.voltaje = voltaje
        self.perdida_calor_lista = []  # Lista para almacenar la pérdida de calor en cada paso de tiempo
        self.temperatura_fluido_lista = []  # Lista para almacenar la temperatura del fluido en cada paso de tiempo

    def set_tiempo(self, tiempo):
        if tiempo > 0:
            self.tiempo = tiempo
        else:
            print("El tiempo debe ser mayor que cero")

    def calcular_perdida_calor(self, coeficiente_conductividad, superficie_total, espesor_pared):
        perdida_calor = coeficiente_conductividad * superficie_total * self.temperatura_fluido / espesor_pared
        return perdida_calor
    
    def simular_calentamiento(self, coeficiente_conductividad, superficie_total, espesor_pared):
        for _ in range(self.tiempo):
            # Calcular la pérdida de calor
            perdida_calor = self.calcular_perdida_calor(coeficiente_conductividad, superficie_total, espesor_pared)
            self.perdida_calor_lista.append(perdida_calor)
            
            # Calcular el calor efectivo entregado al fluido (restar la pérdida de calor)
            calor_efectivo = self.voltaje - perdida_calor
            
            # Calcular la variación de temperatura del fluido
            delta_t = calor_efectivo / (self.masa * self.constante_calor)
            
            # Actualizar la temperatura del fluido
            self.temperatura_fluido += delta_t
            self.temperatura_fluido_lista.append(self.temperatura_fluido)
    
    def graficar_temperatura_fluido(self):
        plt.plot(range(1, self.tiempo + 1), self.temperatura_fluido_lista, 'b-', label='Con Pérdidas')
        plt.plot(range(1, self.tiempo + 1), [self.temperatura_fluido] * self.tiempo, 'r--', label='Sin Pérdidas')
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Temperatura del Fluido (°C)')
        plt.title('Temperatura del Fluido con y sin Pérdidas')
        plt.legend()
        plt.grid(True)
        
        # Ajustar el rango de los ejes
        plt.xlim(1, self.tiempo)
        plt.ylim(min(self.temperatura_fluido_lista) - 5, max(self.temperatura_fluido_lista) + 5)
        
        # Cambiar el formato de los ejes
        plt.xticks(range(0, self.tiempo + 1, 50))
        
        # Mostrar la gráfica
        plt.show()


# Crear instancia del calentador
calentador1 = Calentador(30, 1000, 300, 220)

# Especificaciones del diseño del dispositivo
coeficiente_conductividad = 2.1  # CCT en Watts/metro Kelvin
superficie_total = 1  # Sup en metros cuadrados
espesor_pared = 0.001  # Esp en metros

# Simular el calentamiento con pérdidas
calentador1.simular_calentamiento(coeficiente_conductividad, superficie_total, espesor_pared)

# Graficar la temperatura del fluido con y sin pérdidas
calentador1.graficar_temperatura_fluido()
