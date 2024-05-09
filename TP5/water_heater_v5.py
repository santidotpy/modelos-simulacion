import numpy as np
import matplotlib.pyplot as plt

def temperatura_normal():
    return np.random.normal(10, 5, 5)

def resistencia_uniforme():
    return np.random.uniform(1, 10, 5)

def temperatura_ambiente_uniforme():
    return np.random.uniform(-20, 50, 8)

def tension_alimentacion_normal(tipo_tension):
    if tipo_tension == "media_12":
        return np.random.normal(12, 4, 5)
    elif tipo_tension == "media_220":
        return np.random.normal(220, 40, 5)

def curva_familia(x, parameters):
    a, b, c = parameters
    return a * np.exp(b * x) + c  

# Generar datos para las curvas de familia
resistencias = resistencia_uniforme()
temperaturas_agua = temperatura_normal()
temperaturas_ambiente = temperatura_ambiente_uniforme()

tipos_tension = ["media_12", "media_220"]
tensiones_alimentacion = {}
for tipo_tension in tipos_tension:
    tensiones_alimentacion[tipo_tension] = tension_alimentacion_normal(tipo_tension)

x = np.linspace(0, 10, 100)

# Graficar las curvas de familia
plt.figure(figsize=(10, 8))

subplot_indices = [321, 322, 323, 324, 325]
plot_titles = [
    'Curvas de Familia - Resistencias',
    'Curvas de Familia - Temperatura Ambiente',
    'Curvas de Familia - Temperatura Agua',
    'Curvas de Familia - Tensión de Alimentación (Media 12)',
    'Curvas de Familia - Tensión de Alimentación (Media 220)'
]

data_sets = [
    (resistencias, 'resistencia'),
    (temperaturas_ambiente, 'temperatura_ambiente'),
    (temperaturas_agua, 'temperatura_agua'),
    (tensiones_alimentacion["media_12"], 'tension_12'),
    (tensiones_alimentacion["media_220"], 'tension_220')
]

for subplot_index, plot_title, data_set in zip(subplot_indices, plot_titles, data_sets):
    data, data_type = data_set
    plt.subplot(subplot_index)
    for value in data:
        if data_type == 'resistencia':
            parameters = [value, 0.1, 0.5]
        elif data_type == 'temperatura_agua' or data_type == 'temperatura_ambiente':
            parameters = [1, 0.1, value]
        else:
            parameters = [value, 0.1, 0.5]
        plt.plot(x, curva_familia(x, parameters))
    plt.title(plot_title)

plt.tight_layout()
plt.show()
