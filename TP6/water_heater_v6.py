import numpy as np
import matplotlib.pyplot as plt

def resistencia_uniforme():
    return np.random.uniform(1, 10, 5)

def temperatura_normal():
    return np.random.normal(10, 5, 5)

def temperatura_ambiente_uniforme():
    return np.random.uniform(-20, 50, 8)

def tension_alimentacion_normal(option=1):
    if option == 1:
        return np.random.normal(12, 4, 5)
    elif option == 2:
        return np.random.normal(220, 40, 5)

def curva_familia(x, parametros):
    a, b, c = parametros
    return a * np.exp(b * x) + c 

def simular_descenso(temp_agua_actual, prob_ocurrencia, max_descenso):
    if np.random.random() < prob_ocurrencia:
        descenso = np.random.uniform(0, max_descenso)
        duracion = np.random.randint(1, 60) 
        temp_agua_actual -= descenso
        print(f"Descenso de temperatura: {descenso} grados durante {duracion} segundos.")
    return temp_agua_actual

# Generar datos para las curvas de familia
resistencias = resistencia_uniforme()
temperaturas_agua = temperatura_normal()
temperaturas_ambiente = temperatura_ambiente_uniforme()

tensiones_alimentacion_media_12 = tension_alimentacion_normal(option=1)
tensiones_alimentacion_media_220 = tension_alimentacion_normal(option=2)

x = np.linspace(0, 10, 100)

# Graficar las curvas de familia
plt.figure(figsize=(10, 8))

subplot_titles = [
    'Curvas de Familia - Resistencias',
    'Curvas de Familia - Temperatura del Ambiente',
    'Curvas de Familia - Temperatura del Agua',
    'Curvas de Familia - Tensión de Alimentación (Media 12)',
    'Curvas de Familia - Tensión de Alimentación (Media 220)'
]

subplot_data = [
    (resistencias, 'resistencia'),
    (temperaturas_ambiente, 'temperatura_ambiente'),
    (temperaturas_agua, 'temperatura_agua'),
    (tensiones_alimentacion_media_12, 'tension_media_12'),
    (tensiones_alimentacion_media_220, 'tension_media_220')
]

for i, (data, data_type) in enumerate(subplot_data, start=1):
    plt.subplot(3, 2, i)
    plt.title(subplot_titles[i-1])
    for value in data:
        if data_type == 'resistencia':
            parametros = [value, 0.1, 0.5]
        elif data_type == 'temperatura_agua':
            temp_agua_actual = value
            for j in range(len(x)):
                temp_agua_actual = simular_descenso(temp_agua_actual, 1/300, 50)
                parametros = [1, 0.1, temp_agua_actual]
                plt.plot(x, curva_familia(x, parametros))
        elif data_type == 'temperatura_ambiente':
            parametros = [1, 0.1, value]
            plt.plot(x, curva_familia(x, parametros))
        elif data_type == 'tension_media_12' or data_type == 'tension_media_220':
            parametros = [value, 0.1, 0.5]
            plt.plot(x, curva_familia(x, parametros))

plt.tight_layout()
plt.show()
