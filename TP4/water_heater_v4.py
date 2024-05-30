import matplotlib.pyplot as plt
from data_heater import temperatura_inicial_fluido, temperatura, masa, tiempo, voltaje
from water_heater_v2 import Calentador

# Configuración inicial
resistencia = 50
potencia_resistencia = 968
masa_fluido = 1  # en kg
calor_especifico_fluido = 4186  # en J/(kg*°C)
ticks_por_segundo = 10
ticks_totales = tiempo * ticks_por_segundo

# Inicialización del calentador
calentador1 = Calentador(temperatura, masa, tiempo, voltaje)

def calcular_temperatura(ticks, considerar_perdidas):
    """Calcula la temperatura del fluido con o sin pérdidas."""
    temperatura = temperatura_inicial_fluido
    for _ in range(ticks):
        if considerar_perdidas:
            potencia_efectiva = potencia_resistencia - (temperatura - temperatura_inicial_fluido) * 10
        else:
            potencia_efectiva = potencia_resistencia

        calor_suministrado = potencia_efectiva / ticks_por_segundo
        calor_absorbido = calor_especifico_fluido * masa_fluido
        delta_temperatura = calor_suministrado / calor_absorbido
        temperatura += delta_temperatura
    return temperatura

def generar_datos_temperatura():
    """Genera listas de temperaturas con y sin pérdidas."""
    temperaturas_con_perdidas = [temperatura_inicial_fluido]
    temperaturas_sin_perdidas = [temperatura_inicial_fluido]

    for tick in range(1, ticks_totales + 1):
        temp_con_perdidas = calcular_temperatura(tick, considerar_perdidas=True)
        temp_sin_perdidas = calcular_temperatura(tick, considerar_perdidas=False)
        temperaturas_con_perdidas.append(temp_con_perdidas)
        temperaturas_sin_perdidas.append(temp_sin_perdidas)

    return temperaturas_con_perdidas, temperaturas_sin_perdidas

def graficar_temperaturas(tiempo, temperaturas_con_perdidas, temperaturas_sin_perdidas):
    """Genera una gráfica de las temperaturas con y sin pérdidas a lo largo del tiempo."""
    plt.plot(tiempo, temperaturas_con_perdidas, label='Con pérdidas', color='blue')
    plt.plot(tiempo, temperaturas_sin_perdidas, label='Sin pérdidas', color='red')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Temperatura del agua (°C)')
    plt.title('Temperatura del agua en el calentador')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    # Generar datos de temperatura
    temperaturas_con_perdidas, temperaturas_sin_perdidas = generar_datos_temperatura()
    
    # Lista de tiempo en segundos para cada tick
    tiempo = [i / ticks_por_segundo for i in range(ticks_totales + 1)]
    
    # Graficar los resultados
    graficar_temperaturas(tiempo, temperaturas_con_perdidas, temperaturas_sin_perdidas)

if __name__ == '__main__':
    main()
