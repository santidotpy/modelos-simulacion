import numpy as np
import matplotlib.pyplot as plt

def temperatura_normal(size=5):
    """Genera temperaturas aleatorias con distribución normal."""
    return np.random.normal(10, 5, size)

def curva_familia(x, parametros):
    """Calcula la curva de familia para los parámetros dados."""
    a, b, c = parametros
    return a * np.exp(b * x) + c 

def simular_descenso(temp_agua_actual, probabilidad=1 / 300, max_descenso=50, max_duracion=60):
    """Simula un fenómeno estocástico de descenso de temperatura."""
    if np.random.random() < probabilidad:
        descenso = np.random.uniform(0, max_descenso)
        duracion = np.random.randint(1, max_duracion)
        temp_agua_actual -= descenso
        print(f"Descenso de temperatura: {descenso} grados durante {duracion} segundos.")
    return temp_agua_actual

def main():
    # Generar datos
    temperaturas_agua = temperatura_normal()

    x = np.linspace(0, 10, 100)

    # Graficar las curvas de familia para la temperatura del agua
    plt.figure(figsize=(10, 8))

    for temperatura in temperaturas_agua:
        temp_agua_actual = temperatura
        for _ in range(len(x)):
            temp_agua_actual = simular_descenso(temp_agua_actual)
            parametros = [1, 0.1, temp_agua_actual]
            plt.plot(x, curva_familia(x, parametros))
    plt.title('Curvas de Familia - Temperatura del Agua')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Temperatura del Agua (°C)')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
