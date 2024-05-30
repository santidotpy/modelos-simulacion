import random
import locale
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.stats import truncnorm

# Constantes
HORARIO_APERTURA = 8 * 60 * 60  # 8:00 AM en segundos (28800 segundos)
HORARIO_CIERRE = 12 * 60 * 60  # 12:00 PM en segundos (43200 segundos)
DURACION_JORNADA = HORARIO_CIERRE - HORARIO_APERTURA  # 4 horas en segundos (14400 segundos)
PROBABILIDAD_INGRESO = 1 / 144
MEDIA_ATENCION = 10 * 60  # 10 minutos en segundos (600 segundos)
DESVIO_ATENCION = 5 * 60  # 5 minutos en segundos (300 segundos)
COSTO_BOX = 1000
COSTO_PERDIDA_CLIENTE = 10000

locale.setlocale( locale.LC_ALL, '' )

# Función para generar tiempos de atención positivos
def generar_tiempo_atencion(media, desviacion, min_val=0):
    a, b = (min_val - media) / desviacion, np.inf
    return truncnorm.rvs(a, b, loc=media, scale=desviacion)

# Inicializar variables
clientes_ingresados = 0
clientes_atendidos = 0
clientes_no_atendidos = 0
tiempos_atencion = []
tiempos_espera = []
cola = []

# Parámetros de la simulación
num_boxes = int(input("Ingrese el número de boxes de atención (1-10): "))
boxes = [None] * num_boxes
tiempos_libres = [0] * num_boxes

# Función para simular un segundo
def simular_segundo(segundo):
    global clientes_ingresados, clientes_atendidos, clientes_no_atendidos
    
    # Determinar si ingresa un nuevo cliente
    if random.random() < PROBABILIDAD_INGRESO:
        clientes_ingresados += 1
        cola.append(segundo)
    
    # Atender clientes en boxes
    for i in range(num_boxes):
        if boxes[i] is None and cola:
            tiempo_entrada = cola.pop(0)
            tiempo_atencion = int(generar_tiempo_atencion(MEDIA_ATENCION, DESVIO_ATENCION))
            tiempos_espera.append(segundo - tiempo_entrada)
            boxes[i] = segundo + tiempo_atencion
            tiempos_atencion.append(tiempo_atencion)
            clientes_atendidos += 1
        elif boxes[i] is not None and boxes[i] <= segundo:
            boxes[i] = None
    
    # Clientes abandonan después de 30 minutos sin ser atendidos
    while cola and (segundo - cola[0]) > 30 * 60:
        cola.pop(0)
        clientes_no_atendidos += 1

# Simulación
for segundo in range(HORARIO_APERTURA, HORARIO_CIERRE + 1):
    simular_segundo(segundo)

# Procesar cola después del cierre
segundo = HORARIO_CIERRE
while cola:
    segundo += 1
    simular_segundo(segundo)

def sec_to_min(sec):
    return sec // 60

# Resultados
print(f"Total de clientes ingresados: {clientes_ingresados}")
print(f"Total de clientes atendidos: {clientes_atendidos}")
print(f"Total de clientes no atendidos: {clientes_no_atendidos}")
print(f"Tiempo mínimo de atención en box: {min(tiempos_atencion)} segundos (equivalente a {sec_to_min(min(tiempos_atencion))} minutos)")
print(f"Tiempo máximo de atención en box: {max(tiempos_atencion)} segundos (equivalente a {sec_to_min(max(tiempos_atencion))} minutos)")
print(f"Tiempo mínimo de espera en salón: {min(tiempos_espera)} segundos (equivalente a {sec_to_min(min(tiempos_espera))} minutos)")
print(f"Tiempo máximo de espera en salón: {max(tiempos_espera)} segundos (equivalente a {sec_to_min(max(tiempos_espera))} minutos)")

# Costo de operación
costo_operacion = num_boxes * COSTO_BOX + clientes_no_atendidos * COSTO_PERDIDA_CLIENTE
print(f"Costo total de operación: {locale.currency(costo_operacion, grouping=True)}")

